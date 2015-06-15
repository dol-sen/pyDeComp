
'''
contents.py

Utility class to hold and handle all possible contents
listing of compressed files using native linux utilities.

If you have other contents defintions,
please send them along for inclusion in the main repo.

Maintained in full by:
	Brian Dolbec <dolsen@gentoo.org>

'''

from __future__ import print_function

import os
from subprocess import Popen, PIPE

from DeComp.definitions import (CONTENTS_SEARCH_ORDER, DEFINITION_FIELDS,
	EXTENSION_SEPARATOR)
from DeComp.utils import create_classes, subcmd


class ContentsMap(object):
	'''Class to encompass all known commands to list
	the contents of an archive'''


	'''fields: list of ordered field names for the contents functions
	use ContentsMap.fields for the value legend'''
	fields = DEFINITION_FIELDS[:]


	def __init__(self, definitions=None, env=None, default_mode=None,
			separator=EXTENSION_SEPARATOR, search_order=None):
		'''Class init

		@param definitions: dictionary of
			Key:[function, cmd, cmd_args, Print/id string, extensions]
		@param env: environment to pass to the subprocess
		@param default_mode: string.  one of the defintions keys
		'''
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
		print("ContentsMap: __init__(), search_order = " + str(self.search_order))
		# create the contents definitions namedtuple classes
		self._map = create_classes(definitions, self.fields)


	def contents(self, source, destination, mode="auto", verbose=False):

		if mode in ['auto']:
			mode = self.determine_mode(source)
		func = getattr(self, '%s' % self._map[mode].func)
		return func(source, destination,
			self._map[mode].cmd, self._map[mode].args, verbose)


	def get_extension(self, source):
		'''Extracts the file extension string from the source file

		@param source: string, file path of the file to determine
		@return string: file type extension of the source file
		'''
		return os.path.splitext(source)[1]


	def determine_mode(self, source):
		'''Uses the search_order spec parameter and
		compares the contents file extension strings
		with the source file and returns the mode to use for decompression.

		@param source: string, file path of the file to determine
		@return string: the comtents mode to use on the source file
		'''
		print("ContentsMap: determine_mode(), source = " + source)
		result = None
		for mode in self.search_order:
			print("ContentsMap: determine_mode(), mode = " + mode, self.search_order)
			for ext in self._map[mode].extensions:
				if source.endswith(ext):
					result = mode
					break
			if result:
				break
		if not result:
			print("ContentsMap: determine_mode(), failed to find a mode " +
				"to use for: " + source)
		return result


	@staticmethod
	def _common(source, destination, cmd, args, verbose):
		_cmd = [cmd]
		_cmd.extend((' '.join(args)
			% {'source': source, "destination": destination }).split())
		try:
			proc = Popen(_cmd, stdout=PIPE, stderr=PIPE)
			results = proc.communicate()
			result = "\n".join(results)
		except OSError as e:
			results = ''
			print("ContentsMap: _common(); OSError:" , e, ' '.join(_cmd))
		if verbose:
			print(result)
		return result


	@staticmethod
	def _mountable(source, destination, cmd, args, verbose):
		return 'Code ME!!!!!!'
