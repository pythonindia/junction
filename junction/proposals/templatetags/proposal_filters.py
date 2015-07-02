# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django import template


register = template.Library()


@register.filter(name='reviewer_comments')
def reviewer_comments(proposal, user):
    return proposal.get_reviewer_comments_count(user) > 0
