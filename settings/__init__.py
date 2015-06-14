# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

# Standard Library
import sys
import os

if "test" in sys.argv:
    print("\033[1;91mNo django tests.\033[0m")
    print("Try: \033[1;33mpy.test\033[0m")
    sys.exit(0)

from .common import *  # noqa
from .celery import *  # noqa

try:
    from .dev import *  # noqa
except ImportError:
    pass

try:
    from .prod import *  # noqa
except ImportError:
    pass

# heroku

if 'DYNO' in os.environ:
    from .heroku import *
