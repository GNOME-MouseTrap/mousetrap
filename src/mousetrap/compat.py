"""
Python 2/3 compatibility module.
"""

import sys

PY3 = sys.version_info[0] == 3

if PY3:
    string_types = (str, )
else:
    string_types = (basestring, )
