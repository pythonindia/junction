# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Standard Library
from os import path

# Third Party Stuff
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_email(to, context, template_dir):
    """Render given templates and send email to `to`.

    :param to: User object to send email to..
    :param context: dict containing which needs to be passed to django template
    :param template_dir: We expect files message.txt, subject.txt,
    message.html etc in this folder.
    :returns: None
    :rtype: None

    """
    def to_str(template_name):
        return render_to_string(path.join(template_dir, template_name), context).strip()

    subject = to_str('subject.txt')
    text_message = to_str('message.txt')
    html_message = to_str('message.html')
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [_format_email(to)]

    return send_mail(subject, text_message, from_email, recipient_list, html_message=html_message)


def _format_email(user):
    return user.email if user.first_name and user.last_name else \
        '"{} {}" <{}>'.format(user.first_name, user.last_name, user.email)
