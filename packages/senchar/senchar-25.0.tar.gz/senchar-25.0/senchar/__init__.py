"""
Scientific image sensor characterization package.
"""

import typing
from importlib import metadata
from senchar.database import Database

__version__ = metadata.version(__package__)
__version_info__ = tuple(int(i) for i in __version__.split(".") if i.isdigit())

db = Database()
db.version = __version__

# placeholder for log
log = print

# cleanup namespace
del metadata
del typing
del Database
