# -*- coding: utf-8 -*-
from os import path

from django.conf import settings
from django.template import TemplateDoesNotExist
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_email(to, context, template_dir):
    """Render given templates and send email to `to`.

    :param to: User object to send email to..
    :param context:
    :param template_dir: We expect files message.txt, subject.txt,
    message.html etc in this folder.
    :returns: None
    :rtype: None

    """
    expected_templates = {'message': 'message.txt', 'subject': 'subject.txt',
                          'html_message': 'message.html'}

    kwargs = {key: render_to_string(path.join(template_dir, template),
                                    context).strip()
              for key, template in expected_templates.items()}

    return send_mail(from_email=settings.DEFAULT_FROM_EMAIL,
                     recipient_list=[_format_email(to)], **kwargs)


def _format_email(user):
    return user.email if user.first_name and user.last_name else \
        '"{} {}" <{}>'.format(user.first_name, user.last_name, user.email)
