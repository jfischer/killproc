#!/usr/bin/env python
# Copyright 2011 by Jeff Fischer
# This utility is made available under the Apache V2.0 license,
# see http://www.apache.org/licenses/LICENSE-2.0.html

import sys
import os
import subprocess
from signal import SIGKILL, SIGTERM, NSIG
from optparse import OptionParser


if sys.platform == 'linux2':
  psargs = '-ef'
  pid_field = 1
  cmd_field = 7
else:
  psargs = '-Ax'
  pid_field = 0
  cmd_field = 4

def get_matching_processes(process_name, this_program=sys.argv[0]):
    subproc = subprocess.Popen(["/bin/ps", psargs],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    result = []
    for line in subproc.stdout:
        if (line.find(process_name) != -1):
            if line.find(this_program) != -1:
                continue
            fields = line.split()
            result.append((int(fields[pid_field]), ' '.join(fields[cmd_field:])))
    (pid, exit_status) = os.waitpid(subproc.pid, 0)
    return result

def get_signal_name(signal_no):
    signal_names = {
        SIGKILL: "SIGKILL",
        SIGTERM: "SIGTERM"
    }
    if signal_names.has_key(signal_no):
        return signal_names[signal_no]
    else:
        return str(signal_no)

def kill_procs_interactive(process_name, signal_no):
    matches = get_matching_processes(process_name)
    signame = get_signal_name(signal_no)
    if len(matches)>0:
        cnt = 0
        for (pid, cmd) in matches:
            print "%s" % cmd
            data = raw_input("Kill process %d? [y]" % pid)
            if len(data)==0 or data[0]=="Y" or data[0]=="y":
                print "Sending signal %s to process %d" % (signame, pid)
                os.kill(pid, signal_no)
                cnt = cnt + 1
        print "Sent signal %s to %d processes" % (signame, cnt)
        return 0
    else:
        print "No matches for pattern '%s'" % process_name
        return 1


def kill_procs_noninteractive(process_name, signal_no):
    matches = get_matching_processes(process_name)
    if len(matches)>0:
        cnt = 0
        for (pid, cmd) in matches:
            print "[%d] %s" % (pid, cmd)
            os.kill(pid, signal_no)
            cnt = cnt + 1
        print "Sent signal %s to %d processes" % (get_signal_name(signal_no), cnt)
        return 0
    else:
        print "No matches for pattern '%s'" % process_name
        return 1


def main(argv=sys.argv[1:]):
    usage = "usage: %prog [options] process_name"
    parser = OptionParser(usage=usage)
    parser.add_option("-k", "--with-extreme-prejudice", action="store_true", dest="use_sig_kill",
                      default=False, help="If specified, use SIGKILL (default is SIGTERM)")
    parser.add_option("-s", "--signal", action="store", type="int", dest="signal_no",
                      default=None, help="Use the specified signal. Defaults to %d (SIGTERM)" % SIGTERM)
    parser.add_option("-n", "--non-interactive", action="store_true", dest="non_interactive",
                      default=False, help="If specified, don't ask user for confirmation")
    
    (options, args) = parser.parse_args(args=argv)

    if len(args) == 0:
        parser.print_help()
        return 1
        
    if len(args) > 1:
        parser.error("Expecting exactly one argument: process_name")
    process_name = args[0]

    if options.use_sig_kill and options.signal_no!=None and options.signal_no!=SIGKILL:
        parser.error("Please specify only one of --with-extreme-prejudice and --signal")
    elif options.use_sig_kill:
        signal_no = SIGKILL
    elif options.signal_no!=None:
        if (options.signal_no >= NSIG) or (options.signal_no < 0):
            parser.error("Invalid signal number %d, signals are from 0 to %d" % (options.signal_no, NSIG-1))
        signal_no = options.signal_no
    else:
        signal_no = SIGTERM

    if options.non_interactive:
        return kill_procs_noninteractive(process_name, signal_no)
    else:
        return kill_procs_interactive(process_name, signal_no)


if __name__ == "__main__":
    sys.exit(main())
