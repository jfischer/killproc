=========
killproc
=========

Introduction
============
*killproc* is a command-line utility to terminate or killl Unix processes by name. The standard Unix
*kill* command identifies processes by process id, rather than by process name. For example, to terminate instances of the django-admin.py script, one might use the following sequence::

  $  ps -ef | grep django-admin.py | grep -v grep
  501 20060     1   0   0:00.11 ttys001    0:00.38 /Users/jfischer/apps/python/bin/python /Users/jfischer/apps/python/bin/django-admin.py runserver 0.0.0.0:8002
  501 20063 20060   0   0:00.35 ttys001    0:01.07 /Users/jfischer/apps/python/bin/python /Users/jfischer/apps/python/bin/django-admin.py runserver 0.0.0.0:8002
  $ kill -TERM 20060 20063
  $ ps -ef | grep django-admin.py | grep -v grep

Running the extra *ps* command and picking out process ids from its output can get rather
tedious.

*killproc* automates this sequence: you provide part of a process name and it executes *ps*, filtering
the results by matching the process name fragment with the CMD column of the *ps* output. For each
match, the user is prompted whether they wish to terminate the process (the prompting can be turned
off via a command line option). Accomplishing the above task with *killproc* might look as follows::

  killproc django-admin.py
  /Users/jfischer/apps/python/bin/python /Users/jfischer/apps/python/bin/django-admin.py runserver 0.0.0.0:8002
  Kill process 20106? [y] y
  Sending signal SIGTERM to process 20106
  /Users/jfischer/apps/python/bin/python /Users/jfischer/apps/python/bin/django-admin.py runserver 0.0.0.0:8002
  Kill process 20109? [y] y
  Sending signal SIGTERM to process 20109
  Sent signal SIGTERM to 2 processes


Supported Platforms
===================
*killproc* has been tested on Mac OSX and Ubuntu Linux. It is expected to work on most Linux and BSD variants.


Installation
============
*killproc* is written in Python and packaged using `setuptools <http://pypi.python.org/pypi/setuptools>`_. It has been registered
on `PyPi <http://pipi.python.org/pypi>`_ under *killproc*. Thus, if you have Python and setuptools installed on your machine,
you can run install it via easy_install::

  easy_install killproc

or pip::

  pip killproc

Either command will place the Python package in your Python environment and create the *killproc* script in your Python's binary
directory (thus making it available in your PATH).

The file killproc.py can function as a standalone command line utility. Thus, as an alternative installation approach, you can grab the
killproc.py file out of the source distribution, place it in a directory on your executable path, rename it to killproc, and add execute
permissions.


Usage
=====
The command line format for killproc is::

  killproc [options] process_name

The available options are::

   -h, --help            show help message and exit
   -k, --with-extreme-prejudice
                          If specified, use SIGKILL (default is SIGTERM)
   -s SIGNAL_NO, --signal=SIGNAL_NO
                          Use the specified signal. Defaults to 15 (SIGTERM)
   -n, --non-interactive
                          If specified, don't ask user for confirmation


Caveats, Limitations and Future Enhancements
============================================
Matching processes are not filtered by user. If the processes of other users match the process name fragment, the *killproc*
user will be prompted for those users as well, and the termination of those processes will fail. As a future enhancement,
*killproc* should return only matching processes of the current user by default, with a command line option to return
matches for all users (useful when running as root or sudo).

It would be nice to interpret the process name fragment as a regular expression to be matched against running commands.
However, this should not be the default behavior.
