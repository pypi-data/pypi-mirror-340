=============
Documentation
=============

Submitting a task with MyQueue typically works like this::

    $ mq submit <task> -R <resources>

or::

    $ mq submit "<task> <arguments>" -R <resources>

And checking the result looks like this::

    $ mq list -s <states>  # or just: mq ls

Below, we describe the important concepts :ref:`tasks`, :ref:`arguments`,
:ref:`resources` and :ref:`states`.


.. _tasks:

Tasks
=====

There are five kinds of tasks: :ref:`pymod`, :ref:`pyfunc`, :ref:`pyscript`,
:ref:`shellcmd` and :ref:`shellscript`.


.. _pymod:

Python module
-------------

Examples:

* ``module``
* ``module.submodule`` (a Python submodule)

These are executed as ``python3 -m module`` so Python must be able to import
the modules.


.. _pyfunc:

Function in a Python module
---------------------------

Examples:

* ``module@function``
* ``module.submodule@function``

These are executed as ``python3 -c "import module; module.function(...)`` so
Python must be able to import the function from the module.


.. _pyscript:

Python script
-------------

Examples:

* ``script.py`` (use ``script.py`` in folders where tasks are running)
* ``./script.py`` (use ``script.py`` from folder where tasks were submitted)
* ``/path/to/script.py`` (absolute path)

Executed as ``python3 script.py``.


.. _shellcmd:

Shell command
-------------

Example:

* ``shell:command``

The command must be in ``$PATH``.


.. _shellscript:

Shell-script
------------

Example:

* ``./script``

Executed as ``. ./script``.


.. _arguments:

Arguments
.........

All tasks can take extra arguments by enclosing task and arguments in quotes
like this::

    "<task> <arg1> <arg2> ..."

Arguments will simply be added to the command-line that executes the task,
except for :ref:`pyfunc` tasks where the arguments are converted to Python
literals and passed to the function.  Some examples::

    $ mq submit "script.py ABC 123"

would run ``python3 script.py ABC 123`` and::

    $ mq submit "mymod@func ABC 123"

would run ``python3 -c "import mymod; mymod.func('ABC', 123)``.


.. _venv:

Using a Python virtual environment
==================================

If a task is submitted from a virtual environment then that ``venv`` will also
be activated in the script that runs the task.  MyQueue does this by looking
for an ``VIRTUAL_ENV`` environment variable.


.. _resources:

Resources
=========

A resource specification has the form::

    [use-mpi:]cores[:processes][:gpus][:nodename]:tmax[:weight]

* ``use-mpi``: Use ``p`` (as in parallel) if you want to start your job with
  ``mpiexec``; use ``s`` (as in serial) if you don't.  The default is
  to use ``mpiexec`` unless you have specified ``'use_mpi': False`` in
  your configuration file: :ref:`use_mpi`.

* ``cores``: Number of cores to reserve.

* ``processes``: Number of MPI processes to start
  (defaults to number of cores).

* ``gpus``: Number of GPUs per node to allocate.
  Example: ``4G``.  Default is no GPUs (``0G``).

* ``nodename``: Node-name
  (defaults to best match in :ref:`the list of node-types <nodes>`).

* ``tmax``: Maximum time (use *s*, *m*, *h* and *d* for seconds, minutes,
  hours and days respectively).  Examples: ``1h``, ``2d``.  Default
  is ``10m``.

* ``weight``: weight of a task.  Can be used to limit the number of
  simultaneously running tasks.  See :ref:`task_weight`.
  Defaults to 0.

Both the :ref:`submit <submit>` and :ref:`resubmit <resubmit>` commands
as well as the :func:`myqueue.task.task` function, take
an optional *resources* argument (``-R`` or ``--resources``).
Default resources are a modest one core and 10 minutes.

Examples:

* ``1:1h`` 1 core and 1 process for 1 hour
* ``64:xeon:2d`` 64 cores and 64 processes on "xeon" nodes for 2 days
* ``24:1:30m`` 24 cores and 1 process for 30 minutes
  (useful for OpenMP tasks)
* ``s:24:30m`` 24 cores and 24 processes for 30 minutes
  (useful for tasks that do their own *mpiexec* call)
* ``96:4:4G:10h`` 96 cores and 4 processes and 4 GPUs per node for 10 hours

Resources can also be specified via special comments in scripts:

.. highlight:: python

::

    # MQ: resources=40:1d
    from somewhere import run
    run('something')


.. _preamble:

Preamble
========

The value of the :envvar:`MYQUEUE_PREAMBLE` environment variable
will be inserted at the beginning of the script that will be
submitted.

.. highlight:: bash

.. tip::

   To see the script that you are about to submit, use::

      $ mq submit ... -vz  # --verbose --dry-run


.. _states:

States
======

These are the 8 possible states a task can be in:

==========  ================================================
*queued*    waiting for resources to become available
*hold*      on hold
*running*   actually running
*done*      successfully finished
*FAILED*    something bad happened
*MEMORY*    ran out of memory
*TIMEOUT*   ran out of time
*CANCELED*  a dependency failed or ran out of memory or time
==========  ================================================

The  the ``-s`` or ``--states`` options of the
:ref:`list <list>`, :ref:`resubmit <resubmit>`, :ref:`remove <remove>` and
:ref:`modify <modify>` use the following abbreviations: ``q``, ``h``, ``r``,
``d``, ``F``, ``C``, ``M`` and ``T``. It's also possible to use ``a`` as a
shortcut for the all the "good" states ``qhrd`` and ``A`` for the "bad" ones
``FCMT``.


Examples
========

* Sleep for 2 seconds on 1 core using the :func:`time.sleep()` Python
  function::

    $ mq submit "time@sleep 2" -R 1:1m
    1 ./ time@sleep 2 +1 1:1m
    1 task submitted

* Run the ``echo hello`` shell command in two folders
  (using the defaults of 1 core for 10 minutes)::

    $ mkdir f1 f2
    $ mq submit "shell:echo hello" f1/ f2/
    Submitting tasks: ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2/2
    2 ./f1/ shell:echo hello +1 1:10m
    3 ./f2/ shell:echo hello +1 1:10m
    2 tasks submitted

* Run ``script.py`` on 8 cores for 10 hours::

    $ echo "x = 1 / 0" > script.py
    $ mq submit script.py -R 8:10h
    4 ./ script.py 8:10h
    1 task submitted

You can see the status of your jobs with::

    $ mq list
    id folder name       args  info res.   age state  time error
    ── ────── ────────── ───── ──── ───── ──── ────── ──── ───────────────────────────────────
    1  ./     time@sleep 2     +1   1:1m  0:02 done   0:02
    2  ./f1/  shell:echo hello +1   1:10m 0:00 done   0:00
    3  ./f2/  shell:echo hello +1   1:10m 0:00 done   0:00
    4  ./     script.py             8:10h 0:00 FAILED 0:00 ZeroDivisionError: division by zero
    ── ────── ────────── ───── ──── ───── ──── ────── ──── ───────────────────────────────────
    done: 3, FAILED: 1, total: 4

Remove the failed and done jobs from the list with
(notice the dot meaning the current folder)::

    $ mq remove -s Fd -r .
    1 ./    time@sleep 2     +1 1:1m  0:02 done   0:02
    2 ./f1/ shell:echo hello +1 1:10m 0:00 done   0:00
    3 ./f2/ shell:echo hello +1 1:10m 0:00 done   0:00
    4 ./    script.py           8:10h 0:00 FAILED 0:00 ZeroDivisionError: division by zero
    4 tasks removed

The output files from a task will look like this::

    $ ls -l f2
    total 4
    -rw-rw-r-- 1 jensj jensj 0 Oct 28 10:46 shell:echo.3.err
    -rw-rw-r-- 1 jensj jensj 6 Oct 28 10:46 shell:echo.3.out
    $ cat f2/shell:echo.3.out
    hello

If a job fails or times out, then you can resubmit it with more resources::

    $ mq submit "shell:sleep 4" -R 1:2s
    5 ./ shell:sleep 4 +1 1:2s
    1 task submitted
    $ mq list
    id folder name        args info res.  age state   time
    ── ────── ─────────── ──── ──── ──── ──── ─────── ────
    5  ./     shell:sleep 4    +1   1:2s 0:02 TIMEOUT 0:02
    ── ────── ─────────── ──── ──── ──── ──── ─────── ────
    TIMEOUT: 1, total: 1
    $ mq resubmit -i 5 -R 1:1m
    6 ./ shell:sleep 4 +1 1:1m
    1 task submitted
