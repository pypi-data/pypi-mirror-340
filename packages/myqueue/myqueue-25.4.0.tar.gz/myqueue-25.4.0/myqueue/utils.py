"""Useful utilities."""
from __future__ import annotations

import errno
import os
import re
import sys
import time
from contextlib import contextmanager
from io import StringIO
from math import inf
from pathlib import Path
from types import TracebackType
from typing import IO, Any, Generator

from myqueue.config import Configuration


def mqhome() -> Path:
    """Don't use "~/" when testing."""
    name = os.getenv('MYQUEUE_TESTING')
    if name:
        return Path(name)
    return Path.home()


@contextmanager
def chdir(folder: Path) -> Generator:
    """Temporarily change directory."""
    dir = os.getcwd()
    os.chdir(str(folder))
    yield
    os.chdir(dir)


def str2number(s: str) -> int:
    """Convert GB, GiB, ...

    >>> str2number('1MiB')
    1048576
    >>> str2number('2GB')
    2000000000
    """
    n = re.split('[MG]', s)[0]
    return int(n) * {'MB': 1_000_000,
                     'GB': 1_000_000_000,
                     'M': 1_000_000,
                     'G': 1_000_000_000,
                     'MiB': 1024**2,
                     'GiB': 1024**3}[s[len(n):]]


def opencew(filename: str) -> IO[bytes] | None:
    """Create and open filename exclusively for writing.

    If master cpu gets exclusive write access to filename, a file
    descriptor is returned (a dummy file descriptor is returned on the
    slaves).  If the master cpu does not get write access, None is
    returned on all processors."""

    try:
        fd = os.open(str(filename), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except OSError as ex:
        if ex.errno == errno.EEXIST:
            return None
        raise
    else:
        return os.fdopen(fd, 'wb')


class Lock:
    """File lock."""
    def __init__(self, name: Path, timeout: float = inf):
        self.lock = name
        self.timeout = timeout
        self.locked = False

    def acquire(self) -> None:
        """Wait for lock to become available and then acquire it."""
        t = 0.0
        delta = 0.05
        while True:
            fd = opencew(str(self.lock))
            if fd is not None:
                break
            time.sleep(delta)
            t += delta
            if t > self.timeout:
                raise TimeoutError(self.lock)
            delta *= 2
        self.locked = True

    def release(self) -> None:
        """Release lock."""
        if self.locked:
            self.lock.unlink()
            self.locked = False

    def __enter__(self) -> 'Lock':
        self.acquire()
        return self

    def __exit__(self,
                 type: Exception, value: Exception, tb: TracebackType) -> None:
        self.release()


def plural(n: int, thing: str) -> str:
    """Add "s" to string if needed.

    >>> plural(0, 'hat'), plural(1, 'hat'), plural(2, 'hat')
    ('0 hats', '1 hat', '2 hats')
    """
    if n == 1:
        return '1 ' + thing
    return f'{n} {thing}s'


def is_inside(path1: Path, path2: Path) -> bool:
    """Check if path1 is inside path2.

    >>> is_inside(Path('a/b'), Path('a/'))
    True
    >>> is_inside(Path('a/'), Path('a/b'))
    False
    """
    try:
        path1.relative_to(path2)
    except ValueError:
        return False
    return True


def normalize_folder(folder: Path, root: Path) -> str:
    """Convert folder to string used in SQLite.

    >>> root = Path('/home/user/a/b/')
    >>> normalize_folder(root / 'c', root)
    './c/'
    >>> normalize_folder(root, root)
    './'
    """
    f = str(folder.relative_to(root))
    if f == '.':
        return './'
    return f'./{f}/'


def update_readme_and_completion(test: bool = False) -> None:
    """Update README.rst and commands dict.

    Run this when ever options are changed::

        python3.9+ -m myqueue.utils

    """

    import argparse
    import textwrap

    from myqueue.cli import _main, aliases, commands

    aliases = {command: alias for alias, command in aliases.items()}

    # Path of the complete.py script:
    dir = Path(__file__).parent

    fd = sys.stdout
    sys.stdout = StringIO()

    print('\n.. list-table::')
    print('    :widths: 1 3\n')
    for cmd, (help, description) in commands.items():
        print(f'    * - :ref:`{cmd} <{cmd}>`', end='')
        if cmd in aliases:
            print(f' ({aliases[cmd]})')
        else:
            print()
        print('      -', help.rstrip('.'))

    for cmd, (help, description) in commands.items():
        help = commands[cmd][0].rstrip('.')
        title = f'{cmd.title()}: {help}'
        if cmd in aliases:
            title = title.replace(':', f' ({aliases[cmd]}):')
        print(f'\n\n.. _{cmd}:\n')
        print(f"{title}\n{'-' * len(title)}\n")
        _main(['help', cmd])

    txt = sys.stdout.getvalue()
    txt = txt.replace(':\n\n    ', '::\n\n    ')
    newlines = txt.splitlines()
    sys.stdout = fd

    n = 0
    while n < len(newlines):
        line = newlines[n]
        if line == 'positional arguments:':
            L: list[str] = []
            n += 1
            while True:
                line = newlines.pop(n)
                if not line:
                    break
                if not line.startswith('                '):
                    cmd, _, help = line.strip().partition(' ')
                    L.append(f'{cmd}:\n    {help.strip()}')
                else:
                    L[-1] += ' ' + line.strip()
            newlines[n - 1:n] = L + ['']
            n += len(L)
        n += 1

    if sys.version_info < (3, 10):
        newlines = [line.replace('optional arguments:', 'options:')
                    for line in newlines]

    cli = dir / '..' / 'docs' / 'cli.rst'

    lines = cli.read_text().splitlines()
    a = lines.index('.. computer generated text:')
    if test:
        old = '\n'.join(lines[a + 1:])
        new = '\n'.join(newlines)
        if new != old:
            Path('/tmp/mq.new').write_text(new)
            Path('/tmp/mq.old').write_text(old)
            raise ValueError
    else:
        lines[a + 1:] = newlines
        cli.write_text('\n'.join(lines) + '\n')

    filename = dir / 'complete.py'

    dct: dict[str, list[str]] = {}

    class MyException(Exception):
        pass

    class Parser:
        def __init__(self, **kwargs: Any):
            pass

        def add_argument(self, *args: str, **kwargs: Any) -> None:
            pass

        def add_subparsers(self, **kwargs: Any) -> 'Parser':
            return self

        def add_parser(self, cmd: str, **kwargs: Any) -> 'Subparser':
            return Subparser(cmd)

        def parse_args(self, args: list[str] = None) -> None:
            raise MyException

    class Subparser:
        def __init__(self, command: str):
            self.command = command
            dct[command] = []

        def add_argument(self, *args: str, **kwargs: Any) -> None:
            dct[self.command].extend(arg for arg in args
                                     if arg.startswith('-'))

    AP = argparse.ArgumentParser
    argparse.ArgumentParser = Parser  # type: ignore
    try:
        _main()
    except MyException:
        pass
    finally:
        argparse.ArgumentParser = AP  # type: ignore

    txt = 'commands = {'
    for command, opts in sorted(dct.items()):
        txt += "\n    '" + command + "':\n        ["
        txt += '\n'.join(textwrap.wrap("'" + "', '".join(opts) + "'],",
                                       width=65,
                                       break_on_hyphens=False,
                                       subsequent_indent='         '))
    txt = txt[:-1] + '}'

    lines = filename.read_text().splitlines()

    a = lines.index('# Beginning of computer generated data:')
    b = lines.index('# End of computer generated data')

    if test:
        assert '\n'.join(lines[a + 1:b]) == txt
    else:
        lines[a + 1:b] = [txt]
        filename.write_text('\n'.join(lines) + '\n')


def completion_command() -> str:
    py = sys.executable
    filename = Path(__file__).with_name('complete.py')
    cmd = f'complete -o default -C "{py} {filename}" mq'
    return cmd


def ensure_completions() -> None:
    """Add BASH tab-completion command to activation script."""
    venv = os.environ.get('VIRTUAL_ENV')
    if not venv:
        return
    installed = Path(venv) / 'etc/myqueue/completion-installed'
    if installed.is_file():
        return
    cmd = completion_command()
    activate = Path(venv) / 'bin/activate'
    with activate.open('a') as fd:
        fd.write(f'\n# Tab-completion for MyQueue:\n{cmd}\n')
    installed.parent.mkdir(exist_ok=True, parents=True)
    installed.touch()
    print(f'Just added this line:\n\n  {cmd}\n\nto your {activate} script.\n',
          file=sys.stderr)


def convert_done_files() -> None:
    """Convert old done-files to new-style state files."""
    for path in Path().glob('**/*.done'):
        print(path)
        text = path.read_text()
        if text:
            out = f'{{"state": "done",\n "result": {text}}}\n'
        else:
            out = '{"state": "done"}\n'
        path.with_suffix('.state').write_text(out)
        os.unlink(path)


def get_states_of_active_tasks(folder: Path = None) -> dict[str, str]:
    """Get states of active tasks."""
    from myqueue.queue import Queue
    config = Configuration.read(folder)
    with Queue(config, need_lock=False) as queue:
        active = queue.sql(
            'SELECT folder, name, state FROM tasks '
            'WHERE state IN ("q", "h", "r")')
        return {folder + name: state
                for folder, name, state in active}


if __name__ == '__main__':  # pragma: no cover
    os.environ['COLUMNS'] = '80'
    update_readme_and_completion()
