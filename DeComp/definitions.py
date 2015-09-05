
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

from collections import OrderedDict

DEFINITION_FIELDS = OrderedDict([
    ("func", str),
    ("cmd", str),
    ("args", list),
    ("id", str),
    ("extensions", list)
    ]
)

DEFINITION_HELP = '''
The definition entries are to follow the the definition_types
with the exception of the first entry "Type" which is a mode identifier
for use in the class as a type ID and printable output string.

Definiton entries are composed of the following:
    access key: list of definition fields values.
    eg:
    "tar": [             <== access key: list of DEFINITION_FIELDS
            "_common",   <== the class function that runs the external utility
            "tar",       <==  the external utility command
            ["-cpf", "%(filename)s", "-C", "%(basedir)s", "%(source)s"],
                         ^^  a list of the arguments to pass to the utility
            "TAR",       <== ID string that identifies the utility
            ["tar"]      <==  file extensions list
           ],


Available named string variables that will be substituted with the passed in
values during run time:
"%(filename)s"       filename parameter to pass to the utility
"%(basedir)s"        the base source directory where source originates from
"%(source)s"         the file or directory being acted upon
"%(destination)s"    the destination file or directory
"%(arch)s"           the arch filter to pass in  ie. Available filters: x86,
                     arm, armthumb, powerpc, sparc, ia64
'''


COMPRESS_DEFINITIONS = {
    "Type": ["Compression", "Compression definitions loaded"],
    "rsync": [
                "rsync", "rsync",
                ["-a", "--delete", "%(source)s",  "%(destination)s"],
                "RSYNC", None
             ],
    "lbzip2": [
                "_common", "tar",
                [
                    "-I", "lbzip2", "-cf", "%(filename)s", "-C",
                    "%(basedir)s", "%(source)s"
                ],
                "LBZIP2", ["tar.bz2"]
              ],
    "lbzip2_x": [
                    "_common", "tar",
                    [
                        "--xattrs", "--xattrs-include=security.capability",
                        "--xattrs-include=user.pax.flags", "-I", "lbzip2",
                        "-cf", "%(filename)s", "-C", "%(basedir)s", "%(source)s"
                    ],
                    "LBZIP2", ["tar.bz2"]
                ],
    "bzip2": [
                "_common", "tar",
                ["-cpjf", "%(filename)s", "-C", "%(basedir)s", "%(source)s"],
                "BZIP2", ["tar.bz2"]
             ],
    "bzip2_x": [
                "_common", "tar",
                [
                    "--xattrs", "--xattrs-include=security.capability",
                    "--xattrs-include=user.pax.flags", "-cpjf",
                    "%(filename)s", "-C", "%(basedir)s", "%(source)s",
                ],
                "BZIP2", ["tar.bz2"]
               ],
    "tar": [
                "_common", "tar",
                ["-cpf", "%(filename)s", "-C", "%(basedir)s", "%(source)s"],
                "TAR", ["tar"]
           ],
    "tar_x": [
                "_common", "tar",
                [
                    "--xattrs", "--xattrs-include=security.capability",
                    "--xattrs-include=user.pax.flags", "-cpf",
                    "%(filename)s", "-C", "%(basedir)s", "%(source)s"
                ],
                "TAR", ["tar"]
             ],
    "xz": [
            "_common", "tar",
            ["-cpJf", "%(filename)s", "-C", "%(basedir)s", "%(source)s"],
            "XZ", ["tar.xz"]
          ],
    "xz_x": [
                "_common", "tar",
                [
                    "--xattrs", "--xattrs-include=security.capability",
                    "--xattrs-include=user.pax.flags", "-cpJf",
                    "%(filename)s", "-C", "%(basedir)s", "%(source)s"
                ],
                "XZ", ["tar.xz"]
            ],
    "pixz": [
                "_common", "tar",
                [
                    "-I", "pixz", "-cpf", "%(filename)s", "-C", "%(basedir)s",
                    "%(source)s"
                ],
                "PIXZ", ["tar.xz"]
            ],
    "pixz_x": [
                "_common", "tar",
                [
                    "--xattrs", "--xattrs-include=security.capability",
                    "--xattrs-include=user.pax.flags", "-I", "pixz", "-cpf",
                    "%(filename)s", "-C", "%(basedir)s", "%(source)s"
                ],
                "PIXZ", ["tar.xz"]
              ],
    "gzip": [
                "_common", "tar",
                ["-cpzf", "%(filename)s", "-C", "%(basedir)s", "%(source)s"],
                "GZIP", ["tar.gz"]
            ],
    "gzip_x": [
                "_common", "tar",
                [
                    "--xattrs", "--xattrs-include=security.capability",
                    "--xattrs-include=user.pax.flags", "-cpzf",
                    "%(filename)s", "-C", "%(basedir)s", "%(source)s"
                ],
                "GZIP", ["tar.gz"]
              ],
    "squashfs": [
                    "_sqfs", "mksquashfs",
                    [
                        "%(basedir)s/%(source)s", "%(filename)s", "-comp", "xz",
                        "-Xbcj", "%(arch)s", "-b", "1M"
                    ],
                    "SQUASHFS", ["squashfs", "sfs"]
                ],
    }


DECOMPRESS_DEFINITIONS = {
    "Type":     ["Decompression", "Decompression definitions loaded"],
    "rsync": [
                "rsync", "rsync",
                ["-a", "--delete", "%(source)s", "%(destination)s"],
                "RSYNC", None
             ],
    "lbzip2": [
                "_common", "tar",
                ["-I", "lbzip2", "-xpf", "%(source)s", "-C", "%(destination)s"],
                "LBZIP2", ["tar.bz2", "bz2", "tbz2"]
              ],
    "lbzip2_x": [
                    "_common", "tar",
                    [
                        "--xattrs", "--xattrs-include=security.capability",
                        "--xattrs-include=user.pax.flags", "-I", "lbzip2",
                        "-xpf", "%(source)s", "-C", "%(destination)s"
                    ],
                    "LBZIP2", ["tar.bz2", "bz2", "tbz2"]
                ],
    "bzip2": [
                "_common", "tar",
                ["-xpf", "%(source)s", "-C", "%(destination)s"],
                "BZIP2", ["tar.bz2", "bz2", "tbz2"]
             ],
    "bzip2_x": [
                    "_common", "tar",
                    [
                        "--xattrs", "--xattrs-include=security.capability",
                        "--xattrs-include=user.pax.flags", "-xpf", "%(source)s",
                        "-C", "%(destination)s"
                    ],
                    "BZIP2", ["tar.bz2", "bz2", "tbz2"]
               ],
    "tar": [
                "_common", "tar",
                ["-xpf", "%(source)s", "-C", "%(destination)s"],
                "TAR", ["tar"]
           ],
    "tar_x": [
                "_common", "tar",
                [
                    "--xattrs", "--xattrs-include=security.capability",
                    "--xattrs-include=user.pax.flags", "-xpf", "%(source)s",
                    "-C", "%(destination)s"
                ],
                "TAR", ["tar"]
             ],
    "xz": [
            "_common", "tar",
            ["-xpf", "%(source)s", "-C", "%(destination)s"],
            "XZ", ["tar.xz", "xz"]
          ],
    "xz_x": [
                "_common", "tar",
                [
                    "--xattrs", "--xattrs-include=security.capability",
                    "--xattrs-include=user.pax.flags", "-xpf", "%(source)s",
                    "-C", "%(destination)s"
                ],
                "XZ", ["tar.xz", "xz"]
            ],
    "pixz": [
                "_common", "tar",
                ["-I", "pixz", "-xpf", "%(source)s", "-C", "%(destination)s"],
                "PIXZ", ["tar.xz", "xz"]
            ],
    "pixz_x": [
                "_common", "tar",
                [
                    "--xattrs", "--xattrs-include=security.capability",
                    "--xattrs-include=user.pax.flags", "-I", "pixz", "-xpf",
                    "%(source)s", "-C", "%(destination)s"
                ],
                "PIXZ", ["tar.xz", "xz"]
              ],
    "gzip": [
                "_common", "tar",
                ["-xpzf", "%(source)s", "-C", "%(destination)s"],
                "GZIP", ["tar.gz", "gz"]
            ],
    "gzip_x": [
                "_common", "tar",
                [
                    "--xattrs", "--xattrs-include=security.capability",
                    "--xattrs-include=user.pax.flags", "-xpzf", "%(source)s",
                    "-C", "%(destination)s"
                ],
                "GZIP", ["tar.gz", "gz"]
              ],
    "squashfs": [
                    "_common", "unsquashfs",
                    ["-d", "%(destination)s", "%(basedir)s/%(source)s"],
                    "SQUASHFS", ["squashfs", "sfs"]
                ],
    }


DECOMPRESSOR_SEARCH_ORDER = [
    "pixz", "lbzip2", "squashfs", "gzip", "xz", "bzip2", "tar"
]

DECOMPRESSOR_XATTR_SEARCH_ORDER = [
    "pixz_x", "lbzip2_x", "squashfs", "gzip_x", "xz_x", "bzip2_x", "tar_x"
]

'''Configure this here in case it is ever changed.
This is the only edit point required then.'''
EXTENSION_SEPARATOR = '.'


CONTENTS_DEFINITIONS = {
    "tar": [
                "_common", "tar",
                ["--xattrs", "-tvf", "%(source)s"],
                "TAR", [".tar"]
           ],
    "gzip": [
                "_common", "tar",
                ["--xattrs", "-tvzf", "%(source)s"],
                "GZIP", [".tgz", ".tar.gz", "gz"]
            ],
    "lbzip2": [
                "_common", "tar",
                ["--xattrs", "-I", "lbzip2", "-tvf", "%(source)s"],
                "LBZIP2", [".tbz2", "bz2", ".tar.bz2"]
              ],
    "bzip2": [
                "_common", "tar",
                ["--xattrs", "-tvf", "%(source)s"],
                "BZIP2", [".tbz2", "bz2", ".tar.bz2"]
             ],
    "xz": [
            "_common", "tar",
            ["--xattrs", "-tvf", "%(source)s"],
            "XZ", ["tar.xz", "xz"]
          ],
    "pixz": [
                "_common", "tar",
                ["--xattrs", "-I", "pixz", "-tvf", "%(source)s"],
                "PIXZ", ["tar.xz", "xz"]
            ],
    "isoinfo_l": [
                    "_common", "isoinfo",
                    ["-l", "-i", "%(source)s"],
                    "ISOINFO", []
                 ],
    "isoinfo_f": [
                    "_common", "isoinfo",
                    ["-f", "-i", "%(source)s"],
                    "ISOINFO", []
                 ],
    #"squashfs": [
                    #"_mountable", "mount",
                    #[
                        #"-o", "loop", "-t", "squashfs", "%(source)s",
                        #"%(destination)s"
                    #],
                    #"SQUASHFS", ["squashfs", "sfs"]
                #],
}

# isoinfo_f should be a last resort only
CONTENTS_SEARCH_ORDER = [
    "pixz", "lbzip2", "isoinfo_l", "squashfs",
    "gzip", "xz", "bzip2", "tar", "isoinfo_f"
]
