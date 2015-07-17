# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django import template
import re


register = template.Library()


@register.filter(name='reviewer_comments')
def reviewer_comments(proposal, user):
    return proposal.get_reviewer_comments_count(user) > 0


@register.filter(name='get_content_urls')
def get_content_urls(proposal):
    if proposal.content_urls:
        url_re = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_re, proposal.content_urls)
        return urls
    else:
        return []
