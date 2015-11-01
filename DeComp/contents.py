# -*- coding: utf-8 -*-
"""
contents.py

Utility class to hold and handle all possible contents
listing of compressed files using native linux utilities.

If you have other contents defintions,
please send them along for inclusion in the main repo.

Maintained in full by:
    Brian Dolbec <dolsen@gentoo.org>

"""

from __future__ import print_function

import os
from subprocess import Popen, PIPE

from DeComp.definitions import (CONTENTS_SEARCH_ORDER, DEFINITION_FIELDS,
                                EXTENSION_SEPARATOR)
from DeComp import log
from DeComp.utils import create_classes


class ContentsMap(object):
    """Class to encompass all known commands to list
    the contents of an archive"""


    # fields: list of ordered field names for the contents functions
    # use ContentsMap.fields for the value legend
    fields = list(DEFINITION_FIELDS)


    def __init__(self, definitions=None, env=None, default_mode=None,
                 separator=EXTENSION_SEPARATOR, search_order=None, logger=None):
        """Class init

        :param definitions: dictionary of
            Key:[function, cmd, cmd_args, Print/id string, extensions]
        :type definitions: dictionary
        :param env: environment to pass to the subprocess
        :type env: dictionary
        :param default_mode: one of the defintions keys
        :type default_mode: string
        :param separator: filename extension separator
        :type separator: string
        :param search_order: optional mode search order
        :type search_order: list of strings
        :param logger: optional logging module instance,
                       default: pyDecomp logging namespace instance
        :type logger: logging
        """
        if definitions is None:
            definitions = {}
        self.env = env or {}
        self._map = {}
        self.extension_separator = separator
        # set some defaults depending on what is being loaded
        self.mode = default_mode or 'auto'
        self.search_order = search_order or CONTENTS_SEARCH_ORDER
        if isinstance(self.search_order, str):
            self.search_order = self.search_order.split()
        self.logger = logger or log
        self.logger.info("ContentsMap: __init__(), search_order = %s",
                         str(self.search_order))
        # create the contents definitions namedtuple classes
        self._map = create_classes(definitions, self.fields)


    def contents(self, source, destination, mode="auto", verbose=False):
        """Generate the contens list of the archive

        :param source: optional path to the directory
        :type source: string
        :param destination: optional path to the directory
        :type destination: string
        :param mode: optional mode to use to (de)compress with
        :type mode: string
        :param verbose: toggle
        :type verbose: boolean
        :returns: string, list of the contents
        """
        if mode in ['auto']:
            mode = self.determine_mode(source)
        func = getattr(self, '%s' % self._map[mode].func)
        return func(source, destination,
                    self._map[mode].cmd, self._map[mode].args, verbose)


    @staticmethod
    def get_extension(source):
        """Extracts the file extension string from the source file

        :param source: path to the archive
        :type source: string
        :returns: string: file type extension of the source file
        """
        return os.path.splitext(source)[1]


    def determine_mode(self, source):
        """Uses the search_order spec parameter and compares the contents
        file extension strings with the source file and returns the mode to
        use for contents generation.

        :param source: file path of the file to determine
        :type source: string
        :returns: string: the contents generation mode to use on the source file
        """
        self.logger.debug("ContentsMap: determine_mode(), source = %s", source)
        result = None
        for mode in self.search_order:
            self.logger.debug("ContentsMap: determine_mode(), mode = %s, %s",
                              mode, self.search_order)
            for ext in self._map[mode].extensions:
                if source.endswith(ext):
                    result = mode
                    break
            if result:
                break
        if not result:
            self.logger.debug("ContentsMap: determine_mode(), failed to "
                              "find a mode to use for: %s", source)
        return result


    def _common(self, source, destination, cmd, args, verbose):
        """General purpose controller to generate the contents listing

        :param source: optional path to the directory
        :type source: string
        :param destination: optional path to the directory
        :type destination: string
        :param cmd: definition command to use to generate the contents with
        :type cmd: string
        :param args: optioanl command arguments
        :type args: list
        :param verbose: toggle
        :type verbose: boolean
        :returns: string, list of the contents
        """
        _cmd = [cmd]
        _cmd.extend((' '.join(args)
                     % {'source': source, "destination": destination}
                    ).split()
                   )
        try:
            proc = Popen(_cmd, stdout=PIPE, stderr=PIPE)
            results = proc.communicate()
            stdout = results[0].decode('UTF-8')
            stderr = results[1].decode('UTF-8')
            result = "\n".join([stdout, stderr])
        except OSError as error:
            result = ''
            self.logger.error("ContentsMap: _common(); OSError: %s, %s",
                              str(error), ' '.join(_cmd))
        if verbose:
            self.logger.info(result)
        return result


    @staticmethod
    def _mountable(source, destination, cmd, args, verbose):
        """Controll module to mount/umount a mountable filesystem

        :param source: optional path to the directory
        :type source: string
        :param destination: optional path to the directory
        :type destination: string
        :param cmd: definition command to use to generate the contents with
        :type cmd: string
        :param args: optioanl command arguments
        :type args: list
        :param verbose: toggle
        :type verbose: boolean
        :returns: string, list of the contents
        """
        return 'NOT IMPLEMENTED!!!!!!'
