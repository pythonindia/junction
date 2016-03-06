# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.core.exceptions import PermissionDenied
from django.core.management import call_command
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .forms import SyncDataForm


@require_http_methods(['GET', 'POST'])
def sync_data(request):
    """
    View to call sync_data management command.
    """
    if not request.user.is_superuser:
        raise PermissionDenied

    form = SyncDataForm()

    if request.method == 'GET':
        return render(request, 'sync_data.html', {'form': form})

    call_command('sync_data')
    return render(request, 'sync_data.html',
                  {'form': form, 'message': 'Data synced'})
