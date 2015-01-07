# -*- coding: utf-8 -*-
from __future__ import print_function

# Standard Library
import sys

if "test" in sys.argv:
    print("\033[1;91mNo django tests.\033[0m")
    print("Try: \033[1;33mpy.test\033[0m")
    sys.exit(0)

from .common import *  # noqa

try:
    from .dev import *  # noqa
    from .prod import *  # noqa
except ImportError:
    pass
