#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Flask Quorum
# Copyright (C) 2008-2012 Hive Solutions Lda.
#
# This file is part of Hive Flask Quorum.
#
# Hive Flask Quorum is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Flask Quorum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Flask Quorum. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import sys
import time
import atexit
import signal

class Daemon:
    """
    A generic daemon class that provides the general
    daemon capabilities. In order to inherit the daemon
    capabilities override the run method.
    """

    pidfile = None
    """ The path to the file that will hold the
    pid of the created daemon """

    stdin = None
    """ The file path to the file to be used
    as the standard input of the created process """

    stdout = None
    """ The file path to the file to be used
    as the standard output of the created process """

    stderr = None
    """ The file path to the file to be used
    as the standard error of the created process """

    def __init__(self, pid_file, stdin = "/dev/null", stdout = "/dev/null", stderr = "/dev/null"):
        """
        Constructor of the class.

        @type pidfile: String
        @param pidfile: The path to the pid file.
        @type stdin: String
        @param stdin: The file path to the file to be used
        as the standard input of the created process.
        @type stdout: String
        @param stdout: The file path to the file to be used
        as the standard output of the created process.
        @type stderr: String
        @param stderr: The file path to the file to be used
        as the standard error of the created process.
        """

        self.pidfile = pid_file
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr

    def daemonize(self):
        """
        Do the UNIX double-fork magic, see Stevens "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177).

        This is considered the main method for the execution
        of the daemon strategy.

        @see: http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """

        try:
            pid = os.fork() #@UndefinedVariable
            if pid > 0: sys.exit(0)
        except OSError, e:
            sys.stderr.write("first fork failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # decouples the current process from parent environment
        # should create a new group of execution
        os.chdir("/")
        os.setsid() #@UndefinedVariable
        os.umask(0)

        try:
            # runs the second for and then exits from
            # the "second" parent process
            pid = os.fork() #@UndefinedVariable
            if pid > 0:  sys.exit(0)
        except OSError, e:
            sys.stderr.write("second fork failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, "r")
        so = file(self.stdout, "a+")
        se = file(self.stderr, "a+", 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile, "w+").write("%s\n" % pid)

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        try:
            # checks for a pidfile to check if the daemon
            # already runs, in such case retrieves the pid
            # of the executing daemon
            pid_file = file(self.pidfile, "r")
            pid_contents = pid_file.read().strip()
            pid = int(pid_contents)
        except IOError:
            pid = None
        finally:
            pid_file.close()

        # in case the pid value is loaded, prints an error
        # message to the standard error and exists the current
        # process (avoids duplicated running)
        if pid:
            message = "pidfile %s already exists, daemon already running ?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # daemonizes the current process and then starts
        # the daemon structures (runs the process)
        self.daemonize()
        self.run()

    def stop(self):
        try:
            # checks for a pidfile to check if the daemon
            # already runs, in such case retrieves the pid
            # of the executing daemon
            pid_file = file(self.pidfile, "r")
            pid_contents = pid_file.read().strip()
            pid = int(pid_contents)
        except IOError:
            pid = None
        finally:
            pid_file.close()

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return # not an error in a restart

        try:
            while 1:
                os.kill(pid, signal.SIGTERM) #@UndefinedVariable
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)

    def restart(self):
        """
        Restarts the daemon process stopping it and
        then starting it "again".
        """

        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass
        daemon. It will be called after the process has been
        daemonized by start or restart methods.
        """

        pass
