from __future__ import annotations

import os
import subprocess
from math import ceil

from myqueue.schedulers import Scheduler, SchedulerError
from myqueue.task import Task


class SLURM(Scheduler):
    def submit(self,
               task: Task,
               dry_run: bool = False,
               verbose: bool = False) -> int:
        nodelist = self.config.nodes
        resources = task.resources
        nodes, nodedct = resources.select(nodelist)

        env = []

        cmd = str(task.cmd)

        if not self.should_we_use_mpi(resources):
            cmd = cmd.replace('python3', self.config.serial_python)
        else:
            if 'OMP_NUM_THREADS' not in os.environ:
                env.append(('OMP_NUM_THREADS', '1'))
            mpiexec = self.config.mpiexec
            if 'mpiargs' in nodedct:
                mpiexec += ' ' + nodedct['mpiargs']
            cmd = mpiexec + ' ' + cmd.replace('python3',
                                              self.config.parallel_python)
        ntasks = resources.processes
        cpus_per_task = resources.cores // ntasks

        if not os.access(task.folder, os.W_OK | os.X_OK):
            raise IOError(f'{task.folder} folder not writeable!')

        name = task.cmd.short_name
        sbatch = ['sbatch',
                  f'--job-name={name}',
                  f'--time={ceil(resources.tmax / 60)}',
                  f'--ntasks={ntasks}',
                  f'--cpus-per-task={cpus_per_task}',
                  f'--nodes={nodes}',
                  f'--chdir={task.folder}',
                  f'--output={name}.%j.out',
                  f'--error={name}.%j.err']

        partition = nodedct['nodename']
        if partition:  # allow --partition to be skipped
            sbatch.append(f'--partition={partition}')

        if resources.gpus:
            sbatch.append(f'--gpus-per-node={resources.gpus}')

        extra_args = self.config.extra_args + nodedct.get('extra_args', [])
        sbatch += extra_args

        if task.dtasks:
            ids = ':'.join(str(tsk.id) for tsk in task.dtasks)
            sbatch.append(f'--dependency=afterok:{ids}')

        # Use bash for the script
        script = '#!/bin/bash -l\n'

        # Add environment variables
        if len(env) > 0:
            script += '\n'.join(f'export {name}={val}' for name, val in env)
            script += '\n'

        home = self.config.home
        script += (
            'export MYQUEUE_TASK_ID=$SLURM_JOB_ID\n'
            f'mq={home}/.myqueue/slurm-$MYQUEUE_TASK_ID\n')

        script += self.preamble() + '\n'

        script += (
            '(touch $mq-0 && \\\n'
            f' cd {str(task.folder)!r} && \\\n'
            f' {cmd} && \\\n'
            ' touch $mq-1) || \\\n'
            '(touch $mq-2; exit 1)\n')

        if dry_run:
            if verbose:
                print(' \\\n    '.join(sbatch))
                print(script)
            return 1

        # Use a clean set of environment variables without any MPI stuff:
        p = subprocess.run(sbatch,
                           input=script.encode(),
                           capture_output=True,
                           env=os.environ)

        if p.returncode:
            raise SchedulerError((p.stderr + p.stdout).decode())

        return int(p.stdout.split()[-1].decode())

    def cancel(self, id: int) -> None:
        subprocess.run(['scancel', str(id)])

    def hold(self, id: int) -> None:
        subprocess.run(['scontrol', 'hold', str(id)])

    def release_hold(self, id: int) -> None:
        subprocess.run(['scontrol', 'release', str(id)])

    def get_ids(self) -> set[int]:
        user = os.environ.get('USER', 'test')
        cmd = ['squeue', '--user', user]
        p = subprocess.run(cmd, stdout=subprocess.PIPE)
        queued = {int(line.split()[0].decode())
                  for line in p.stdout.splitlines()[1:]}
        return queued

    def maxrss(self, id: int) -> int:
        cmd = ['sacct',
               '-j', str(id),
               '-n',
               '--units=K',
               '-o', 'MaxRSS']
        try:
            p = subprocess.run(cmd, stdout=subprocess.PIPE)
        except FileNotFoundError:
            return 0
        mem = 0
        for line in p.stdout.splitlines():
            line = line.strip()
            if line.endswith(b'K'):
                mem = max(mem, int(line[:-1]) * 1000)
        return mem

    def get_config(self, queue: str = '') -> tuple[list[tuple[str, int, str]],
                                                   list[str]]:
        cmd = ['sinfo',
               '--noheader',
               '-O',
               'CPUs,Memory,Partition']
        p = subprocess.run(cmd, stdout=subprocess.PIPE)
        nodes = []
        for line in p.stdout.decode().splitlines():
            cores, mem, name = line.split()
            nodes.append((name.rstrip('*'),
                          int(cores),
                          mem.rstrip('+') + 'M'))
        return nodes, []
