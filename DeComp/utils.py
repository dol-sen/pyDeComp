'''
Utility functions
'''

from __future__ import print_function

import sys
from collections import namedtuple
from subprocess import Popen


BASH_CMD = "/bin/bash"


def create_classes(definitions, fields):
	'''This function dynamically creates the namedtuple classes which are
	used for the information they contain in a consistent manner.

	@parm definitions: dict, of (de)compressor definitions
		see DEFINITION_FIELDS and DEFINTITION_TYPES defined in this
		library.
	@param fields: list of the field names to create
	@return class_map: dictionary of key: namedtuple class instance
	'''
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


def subcmd(command, exc="", env={}, debug=False):
	#print("***** cmd()")
	sys.stdout.flush()
	args=[BASH_CMD]
	if debug:
		args.append("-x")
	args.append("-c")
	args.append(command)
	print("$$$$$$$", args)
	if debug:
		print("***** subcmd(); args =", args)
	try:
		proc = Popen(args, env=env)
	except:
		raise
	if proc.wait() != 0:
		print("subcmd() NON-zero return value from: %s" % exc)
		return False
	return True


