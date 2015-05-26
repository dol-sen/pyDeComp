
'''
definitions.py

Definitions file to hold and handle all possible compression,
decompression and contents definitions dictionaries for native
linux utilities.  They are used by the compress.py and contents.py classes.

If you have other contents defintions,
please send them along for inclusion in the main repo.

Maintained in full by:
	Brian Dolbec <dolsen@gentoo.org>

'''

DEFINITION_FIELDS = ["func", "cmd", "args", "id", "extensions"]
DEFINITION_TYPES =  [ str,    str,   list,   str,  list]

DEFINITION_HELP = \
'''The definition entries are to follow the the definition_types
with the exception of the first entry "Type" which is a mode identifier
for use in the class as a type ID and printable output string.

Definiton entries are composed of the following:
    access key: list of definition fields values.
    eg:
    "tar"       :["_common", "tar", ["-cpf", "%(filename)s", "-C", "%(basedir)s", "%(source)s"], "TAR", ["tar"]],
    access key  : list of DEFINITION_FIELDS
                 ["func", <== the class function to use to run the external utility with
                             "cmd", <==  the external utility command
                                     "args", <==  a list of the arguments to pass to the utility
                                                                                                  "id", <== ID string that identifies the utility
                                                                                                        "extensions"], <== the list of file extensions this command handles

Available named string variables that will be substituted with the passed in
values during run time:
"%(filename)s"      filename parameter to pass to the utility
"%(basedir)s"       the base source directory where source originates from
"%(source)s"        the file or directory being acted upon
"%(destination)s"   the destination file or directory
"%(arch)s"          the arch filter to pass in  ie. Available filters: x86, arm, armthumb, powerpc, sparc, ia64
'''


COMPRESS_DEFINITIONS = {
	"Type"      :["Compression", "Compression definitions loaded"],
	"rsync"     :["rsync", "rsync", ["-a", "--delete", "%(source)s",  "%(destination)s"], "RSYNC", None],
	"lbzip2"    :["_common", "tar", ["-I", "lbzip2", "-cf", "%(filename)s", "-C", "%(basedir)s", "%(source)s"], "LBZIP2", ["tar.bz2"]],
	"bzip2"     :["_common", "tar", ["-cpjf", "%(filename)s", "-C", "%(basedir)s", "%(source)s"], "BZIP2", ["tar.bz2"]],
	"tar"       :["_common", "tar", ["-cpf", "%(filename)s", "-C", "%(basedir)s", "%(source)s"], "TAR", ["tar"]],
	"xz"        :["_common", "tar", ["-cpJf", "%(filename)s", "-C", "%(basedir)s", "%(source)s"], "XZ", ["tar.xz"]],
	"pixz"      :["_common", "tar", ["-I", "pixz", "-cpf", "%(filename)s", "-C", "%(basedir)s", "%(source)s"], "PIXZ", ["tar.xz"]],
	"gzip"      :["_common", "tar", ["-cpzf", "%(filename)s", "-C", "%(basedir)s", "%(source)s"], "GZIP", ["tar.gz"]],
	"squashfs"  :["_sqfs", "mksquashfs", ["%(basedir)s/%(source)s", "%(filename)s", "-comp", "xz", "-Xbcj", "%(arch)s", "-b", "1M"], "SQUASHFS", ["squashfs", "sfs"]],
	}


DECOMPRESS_DEFINITIONS = {
	"Type"      :["Decompression", "Decompression definitions loaded"],
	"rsync"     :["rsync", "rsync", ["-a", "--delete", "%(source)s", "%(destination)s"], "RSYNC", None],
	"lbzip2"    :["_common", "tar", ["-I", "lbzip2", "-xpf", "%(source)s", "-C", "%(destination)s"], "LBZIP2", ["tar.bz2", "bz2", "tbz2"]],
	"bzip2"     :["_common", "tar", ["-xpf", "%(source)s", "-C", "%(destination)s"], "BZIP2", ["tar.bz2", "bz2", "tbz2"]],
	"tar"       :["_common", "tar", ["-xpf", "%(source)s", "-C", "%(destination)s"], "TAR", ["tar"]],
	"xz"        :["_common", "tar", ["-xpf", "%(source)s", "-C", "%(destination)s"], "XZ", ["tar.xz", "xz"]],
	"pixz"      :["_common", "tar", ["-I", "pixz", "-xpf", "%(source)s", "-C", "%(destination)s"], "PIXZ", ["tar.xz", "xz"]],
	"gzip"      :["_common", "tar", ["-xpzf", "%(source)s", "-C", "%(destination)s"], "GZIP", ["tar.gz", "gz"]],
	"squashfs"  :["_common", "unsquashfs", ["-d", "%(destination)s", "%(basedir)s/%(source)s"], "SQUASHFS", ["squashfs", "sfs"]],
	}


'''Configure this here in case it is ever changed.
This is the only edit point required then.'''
EXTENSION_SEPARATOR = '.'


