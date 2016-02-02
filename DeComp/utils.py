# -*- coding: utf-8 -*-
"""
Utility functions
"""

from __future__ import print_function

import sys
from collections import namedtuple
from subprocess import Popen, PIPE

from DeComp import log

BASH_CMD = "/bin/bash"


def _is_available(self, available_binaries):
    """Private function for the named tuple classes

    :param available_binaries: the confirmed installed binaries
    :type: available_binaries: set
    :returns: boolean
    """
    return self.binaries.issubset(available_binaries)


def create_classes(definitions, fields):
    """This function dynamically creates the namedtuple classes which are
    used for the information they contain in a consistent manner.

    :param definitions: (de)compressor definitions
        see DEFINITION_FIELDS defined in this library.
    :type definitions: dictionary
    :param fields: list of the field names to create
    :type fields: list
    :returns: class_map: dictionary of key: namedtuple class instance
    """
    class_map = {}
    for name in list(definitions):
        # create the namedtuple class instance
        obj = namedtuple(name, fields)
        # reduce memory used by limiting it to the predefined fields variables
        obj.__slots__ = ()
        obj.enabled = _is_available
        # now add the instance to our map
        class_map[name] = obj._make(definitions[name])
    del obj
    return class_map


def subcmd(command, exc="", env=None, debug=False):
    """General purpose function to run a command in a subprocess

    :param command: command string to run
    :type command: string
    :param exc: command name being run (used for the log)
    :type exc: string
    :param env: the environment to run the command in
    :type env: dictionary
    :param debug: optional default: False
    :type debug: boolean
    :returns: boolean
    """
    env = env or {}
    sys.stdout.flush()
    args = [BASH_CMD]
    if debug:
        args.append("-x")
    args.append("-c")
    args.append(command)
    log.debug("subcmd(); args = %s", args)
    try:
        proc = Popen(args, env=env)
    except:
        raise
    if proc.wait() != 0:
        log.debug("subcmd() NON-zero return value from: %s", exc)
        return False
    return True

def check_available(commands):
    """Checks for the available binaries

    :param commands: the binaries to check for their existence
    :type commands: list
    :returns: set of the installed binaries available
    """
    cmd = ["which"]
    cmd.extend(commands)
    proc = None
    try:
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        results = proc.communicate()
        stdout = results[0].decode('UTF-8')
    except OSError as error:
        stdout = ''
        log.error("utils: check_available(); OSError: %s, %s",
                  str(error), ' '.join(cmd))
    finally:
        if proc:
            for pipe in [proc.stdout, proc.stderr]:
                if pipe:
                    pipe.close()
    available = set([x.rsplit('/', 1)[1] for x in stdout.split('\n') if x])
    return available
