# -*- coding: utf-8 -*-
"""
Utility functions
"""

from __future__ import print_function

import sys
from collections import namedtuple
from subprocess import Popen

from DeComp import log

BASH_CMD = "/bin/bash"


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
