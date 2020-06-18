# -*- coding: utf-8 -*-

"""
compress.py

Utility class to hold and handle all possible compression
and de-compression of files using native linux utilities.
Including rsync transfers.

If you have other compression or de-compression defintions,
please send them along for inclusion in the main repo.

Maintained in full by:
    Brian Dolbec <dolsen@gentoo.org>

"""

import os

from DeComp.definitions import (DEFINITION_FIELDS, EXTENSION_SEPARATOR,
    COMPRESSOR_PROGRAM_OPTIONS, DECOMPRESSOR_PROGRAM_OPTIONS,
    DEFAULT_TAR)
from DeComp import log
from DeComp.utils import create_classes, subcmd, check_available


class CompressMap(object):
    """Class for handling
    compression & decompression of archives"""

    # fields: list of ordered field names for the (de)compression functions
    fields = list(DEFINITION_FIELDS)


    def __init__(self, definitions=None, env=None, default_mode=None,
                 separator=EXTENSION_SEPARATOR, search_order=None, logger=None,
                 comp_prog=COMPRESSOR_PROGRAM_OPTIONS[DEFAULT_TAR],
                 decomp_opt=DECOMPRESSOR_PROGRAM_OPTIONS[DEFAULT_TAR]
                ):
        """Class init

        :param definitions: dictionary of
            Key:[function, cmd, cmd_args, Print/id string, extensions]
        :type definitions: dictionary
        :param env: environment to pass to the cmd subprocess
        :type env: dictionary
        :param default_mode: one of the definitions keys
        :type default_mode: string
        :param separator: filename extension separator
        :type separator: string
        :param search_order: optional mode search order
        :type search_order: list of strings
        :param logger: optional logging module instance,
                       default: pyDecomp logging namespace instance
        :type logger: logging
        :param comp_prog: the tar option string to use for the commpressor program
                          bsd's tar is different that linux's tar default: '-I'
        :type comp_prog: string
        :param decomp_opt: external decompressor module option
        :type decomp_opt: string
        """
        if definitions is None:
            definitions = {}
            self.loaded_type = ["None", "No definitions loaded"]
        else:
            self.loaded_type = definitions.pop('Type')
        self.env = env or {}
        self.mode_error = self.loaded_type[0] + \
            " Error: No mode was passed in or automatically detected"
        self._map = {}
        self.extension_separator = separator
        # set some defaults depending on what is being loaded
        if self.loaded_type[0] in ['Compression']:
            self.mode = default_mode or 'tbz2'
            self.compress = self._compress
            self.extract = None
        else:
            self.mode = default_mode or 'auto'
            self.compress = None
            self.extract = self._extract
        self.search_order = search_order or list(definitions)
        if isinstance(self.search_order, str):
            self.search_order = self.search_order.split()
        self.logger = logger or log
        self.comp_prog = comp_prog
        self.decomp_opt = decomp_opt
        self.logger.info("COMPRESS: __init__(), search_order = %s",
                         str(self.search_order))
        # create the (de)compression definition namedtuple classes
        self._map = create_classes(definitions, self.fields)
        binaries = set()
        for mode in self.search_order:
            binaries.update(self._map[mode].binaries)
        self.available = check_available(binaries)


    def _compress(self, infodict=None, filename='', source=None,
                  basedir='.', mode=None, auto_extension=False,
                  arch=None, other_options=None):
        """Compression function

        :param infodict: optional dictionary of the next 4 parameters.
        :type infodict: dictionary
        :param filename: optional name of the file to make
        :type filename: string
        :param source: optional path to the directory
        :type source: string
        :param destination: optional path to the directory
        :type destination: string
        :param mode: optional mode to use to (de)compress with
        :type mode: string
        :param auto_extension: optional, enables or disables
            adding the normaL file extension defined by the mode used.
            defaults to False
        :type auto_extension: boolean
        :returns: boolean
        """
        if not infodict:
            infodict = self.create_infodict(source, None, basedir, filename,
                                            mode or self.mode, auto_extension,
                                            arch, other_options)
        if not infodict['mode']:
            self.logger.error(self.mode_error)
            return False
        if infodict['mode'].endswith("_x"):
            self.logger.warning("Deprecation Warning, all (de)compressor modes "
                                "ending with '_x'")
            self.logger.warning("Please use the 'other_options' capability in "
                                "the non '*_x' modes")
        self.logger.debug("other_options: %s", infodict['other_options'])
        if auto_extension:
            infodict['auto-ext'] = True
        self.logger.debug("CompressMap, Running compression process: %s",
                          infodict['mode'])
        return self._run(infodict)


    def _extract(self, infodict=None, source=None, destination=None,
                 mode=None, other_options=None):
        """De-compression function

        :param infodict: optional dictionary of the next 3 parameters.
        :type infodict: dictionary
        :param source: optional path to the directory
        :type source: string
        :param destination: optional path to the directory
        :type destination: string
        :param mode: optional mode to use to (de)compress with
        :type mode: string
        :returns: boolean
        """
        if self.loaded_type[0] not in ["Decompression"]:
            return False
        if mode or infodict['mode']:
            mode = mode or infodict['mode']
            if mode.endswith("_x"):
                self.logger.warning("Deprecation Warning, all (de)compressor "
                                    "modes ending with '_x'")
                self.logger.warning("Please use the 'other_options' "
                                    "capability in the non '*_x' modes")
        self.logger.debug("other_options: %s", infodict['other_options'])
        if not infodict:
            infodict = self.create_infodict(source, destination, mode=mode,
                                            other_options=other_options)
        if infodict['mode'] in [None]:
            infodict['mode'] = self.mode or 'auto'
        if infodict['mode'] in ['auto']:
            infodict['mode'] = self.determine_mode(infodict['source'])
            if not infodict['mode']:
                self.logger.error(self.mode_error)
                return False
        self.logger.debug("CompressMap, Running extraction process %s",
                          infodict['mode'])
        return self._run(infodict)


    def _run(self, infodict):
        """Internal function that runs the designated function

        :param infodict: optional dictionary of the next 3 parameters.
        :type infodict: dictionary
        :returns: boolean
        """
        if not self.is_supported(infodict['mode']):
            self.logger.error("mode: %s is not supported in the current %s "
                              "definitions", infodict['mode'],
                              self.loaded_type[1]
                             )
            return False
        _func = self._map[infodict['mode']].func
        try:
            # see if it is an internal function name (string)
            # or an external function pointer
            if isinstance(_func, str):
                self.logger.debug("Compress: _run() func is a string: '%s'",
                                  _func)
                func = getattr(self, _func, None)
            else:
                self.logger.debug("Compress: _run(); func is a function: '%s'",
                                  _func)
                func = _func
            success = func(infodict)
        except AttributeError:
            self.logger.error("FAILED to find or run function '%s'",
                              str(self._map[infodict['mode']].func))
            return False
        #except Exception as e:
            #msg = "Error performing %s %s, " % (mode, self.loaded_type[0]) + \
                #"is the appropriate utility installed on your system?"
            #print(msg)
            #print("Exception:", e)
            #return False
        return success


    @staticmethod
    def get_extension(source):
        """Extracts the file extension string from the source file

        :param source: path to the file
        :type source: string
        :returns: string: file type extension of the source file
        """
        return os.path.splitext(source)[1]


    def determine_mode(self, source):
        """Uses the decompressor_search_order spec parameter and
        compares the decompressor's file extension strings
        with the source file and returns the mode to use for decompression.

        :param source: file path of the file to determine
        :type source: string
        :returns: string: the decompressor mode to use on the source file
        """
        self.logger.info("COMPRESS: determine_mode(), source = %s", source)
        result = None
        for mode in self.search_order:
            self.logger.debug("COMPRESS: determine_mode(), mode = %s, %s",
                              mode, self.search_order)
            for ext in self._map[mode].extensions:
                if source.endswith(ext) and \
                   self._map[mode].enabled(self.available):
                    result = mode
                    break
            if result:
                self.logger.debug("COMPRESS: determine_mode(), mode = %s", mode)
                break
        if not result:
            self.logger.warning("COMPRESS: determine_mode(), failed to find a "
                                "mode to use for: %s", source)
        return result


    def rsync(self, infodict=None, source=None, destination=None,
              mode=None):
        """Convienience function. Performs an rsync transfer

        :param infodict: optional dictionary of the next 3 parameters.
        :type infodict: dictionary
        :param source: optional path to the directory
        :type source: string
        :param destination: optional path to the directory
        :type destination: string
        :param mode: optional mode to use to (de)compress with
        :type mode: string
        :returns: boolean
        """
        if not infodict:
            if not mode:
                mode = 'rsync'
            infodict = self.create_infodict(source, destination, mode=mode)
        return self._common(infodict)


    def _common(self, infodict):
        """Internal function.  Performs commonly supported
        compression or decompression commands.

        :param infodict: dict as returned by this class's create_infodict()
        :type infodict: dictionary
        :returns: boolean
        """
        if not infodict['mode'] or not self.is_supported(infodict['mode']):
            self.logger.error("ERROR: CompressMap; %s mode: %s not correctly "
                              "set!", self.loaded_type[0], infodict['mode']
                             )
            return False

        # Avoid modifying the source dictionary
        cmdinfo = infodict.copy()

        # obtain the pointer to the mode class to use
        cmdlist = self._map[cmdinfo['mode']]

        # for compression, add the file extension if enabled
        if cmdinfo['auto-ext']:
            cmdinfo['filename'] += self.extension_separator + \
                self.extension(cmdinfo["mode"])

        cmdargs = self._sub_other_options(cmdlist.args, cmdinfo)

        # Do the string substitution
        opts = ' '.join(cmdargs) %(cmdinfo)
        args = ' '.join([cmdlist.cmd, opts])

        self.logger.debug("COMPRESS: _common(); command args: %s", args)
        # now run the (de)compressor command in a subprocess
        # return it's success/fail return value
        return subcmd(args, cmdlist.id, env=self.env)


    def create_infodict(self, source, destination=None, basedir=None,
                        filename='', mode=None, auto_extension=False,
                        arch=None, other_options=None):
        """Puts the source and destination paths into a dictionary
        for use in string substitution in the defintions
        %(source) and %(destination) fields embedded into the commands

        :param source: path to the directory
        :type source: string
        :param destination: optional path to the directory
        :type destination: string
        :param basedir: optional path to a directory
        :type basedir: string
        :param filename: optional name of the file
        :type filename: string
        :param mode: optional mode to use to (de)compress with
        :type mode: string
        :param auto_extension: optional, enables or disables
            adding the normaL file extension defined by the mode used.
            defaults to False
        :type auto_extension: boolean
        :param arch: optional arch to specify to the compressor
        :type arch: string
        :param other_options: other optional args to pass if the definition
                              supports that attribute
        :type other_options, string or list
        :returns: dictionary
        """
        return {
            'source': source,
            'destination': destination,
            'basedir': basedir,
            'filename': filename,
            'arch': arch or '',
            'mode': mode or self.mode,
            'auto-ext': auto_extension,
            'other_options': other_options,
            'comp_prog': self.comp_prog,
            'decomp_opt': self.decomp_opt,
            }


    def is_supported(self, mode):
        """Truth function to test the mode desired is supported
        in the definitions loaded

        :param mode: string, mode to use to (de)compress with
        :type mode: string
        :returns: boolean
        """
        return mode in list(self._map)


    @property
    def available_modes(self):
        """Convienence function to return the available modes

        :returns: list of modes supported
        """
        return list(self._map)


    def extension(self, mode, all_extensions=False):
        """Returns the predetermined extension auto-ext added
        to the filename for compression.

        :param mode: the compression mode
        :type mode: string
        :param all_extensions: optional, default: False
        :type all_extensions: boolean
        :returns: string
        """
        if self.is_supported(mode):
            if all_extensions:
                return self._map[mode].extensions
            else:  # return the first one (default)
                return self._map[mode].extensions[0]
        return ''


    def _sqfs(self, infodict):
        """Internal function.  Performs commonly supported
        compression or decompression commands.

        :param infodict: dict as returned by this class's create_infodict()
        :type infodict: dictionary
        :returns: boolean
        """

        if not infodict['mode'] or not self.is_supported(infodict['mode']):
            self.logger.error("ERROR: CompressMap; %s mode: %s not correctly "
                              "set!", self.loaded_type[0], infodict['mode']
                             )
            return False

        # Avoid modifying the source dictionary
        cmdinfo = infodict.copy()

        # obtain the pointer to the mode class to use
        cmdlist = self._map[cmdinfo['mode']]

        # for compression, add the file extension if enabled
        if cmdinfo['auto-ext']:
            cmdinfo['filename'] += self.extension_separator + \
                self.extension(cmdinfo["mode"])

        sqfs_opts = self._sub_other_options(cmdlist.args, cmdinfo)
        if not infodict['arch']:
            sqfs_opts.remove("-Xbcj")
            sqfs_opts.remove("%(arch)s")
        opts = ' '.join(sqfs_opts) % (cmdinfo)
        args = ' '.join([cmdlist.cmd, opts])

        # now run the (de)compressor command in a subprocess
        # return it's success/fail return value
        return subcmd(args, cmdlist.id, env=self.env)


    def search_order_extensions(self, search_order):
        """Returns the ordered extension list determined by
        the search order for the (de)compression.

        :param search_order:
        :type search_order: list of strings
        :returns: an ordered list
        """
        seen = set()
        ext_list = []
        for mode in search_order:
            if self.is_supported(mode):
                for ext in self._map[mode].extensions:
                    if ext not in seen:
                        ext_list.append(ext)
                        seen.add(ext)
        return ext_list

    @staticmethod
    def _sub_other_options(args, cmdinfo):
        '''Substitute any other_options in the '''
        cmdargs = args[:]
        # replace the other_options placeholder
        if 'other_options' in cmdargs:
            if isinstance(cmdinfo['other_options'], str):
                if not cmdinfo['other_options']:
                    cmdargs.remove('other_options')
                else:
                    index = cmdargs.index('other_options')
                    cmdargs[index] = cmdinfo['other_options']
            else: # assume it is an iterable
                if not cmdinfo['other_options']:
                    cmdargs.remove('other_options')
                else:
                    index = cmdargs.index('other_options')
                    cmdargs[index] = ' '.join(cmdinfo['other_options'])
        # remove any null strings
        cmdargs = [x for x in cmdargs if x]
        return cmdargs
