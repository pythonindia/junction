# -*- coding: utf-8 -*-

import pytest
from django.core.urlresolvers import reverse
from .. import factories as f
from . import helpers

pytestmark = pytest.mark.django_db


class TestReviewerViews:
    def test_reviewer_private_comment(self, settings, login, conferences,
                                      create_proposal):
        client = login[0]
        conference = conferences['future']

        proposal = create_proposal

        kwargs = {'conference_slug': conference.slug,
                  'proposal_slug': proposal.slug}
        url = reverse('proposal-comment-create', kwargs=kwargs)
        data = {'comment': 'Test', 'private': True}

        response = client.post(url, data)

        assert response.status_code == 302
        assert response.url.endswith('#js-reviewers')

    def test_reviewer_only_private_comment(self, settings, login, conferences,
                                           create_proposal):
        client = login[0]
        conference = conferences['future']

        proposal = create_proposal

        kwargs = {'conference_slug': conference.slug,
                  'proposal_slug': proposal.slug}
        url = reverse('proposal-comment-create', kwargs=kwargs)
        data = {'comment': 'Test', 'reviewer': True}

        response = client.post(url, data)

        assert response.status_code == 302
        assert response.url.endswith('#js-only-reviewers')

    def test_get_review_proposal_form(self, settings, login, conferences,
                                      create_reviewer, create_proposal):
        client = login[0]
        conference = conferences['future']

        proposal = create_proposal

        kwargs = {'conference_slug': conference.slug, 'slug': proposal.slug}
        url = reverse('proposal-review', kwargs=kwargs)

        response = client.get(url)
        context = response.context

        assert response.status_code == 200
        assert context['proposal'] == proposal
        helpers.assert_template_used(response, 'proposals/review.html')

    def test_post_review_proposal(self, settings, login, conferences,
                                  create_reviewer, create_proposal):
        client = login[0]
        conference = conferences['future']

        proposal = create_proposal

        kwargs = {'conference_slug': conference.slug, 'slug': proposal.slug}
        url = reverse('proposal-review', kwargs=kwargs)

        response = client.post(url, {'review_status': 3})

        assert response.status_code == 302

    def test_review_proposal_by_non_reviewer(self, settings, client,
                                             conferences, create_proposal):
        username, password = "temp", "temp"
        f.create_user(password=password, username=username)
        conference = conferences['future']
        client.login(username=username, password=password)
        proposal = create_proposal

        kwargs = {'conference_slug': conference.slug, 'slug': proposal.slug}
        url = reverse('proposal-review', kwargs=kwargs)

        response = client.get(url)

        assert response.status_code == 403
