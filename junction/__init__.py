# -*- coding: utf-8 -*-
__version__ = '0.3.2'
__version_info__ = tuple([int(num) if num.isdigit() else num for num in __version__.replace('-', '.', 1).split('.')])

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery_app import app as celery_app  # noqa
