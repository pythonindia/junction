# -*- coding: utf-8 -*-

import pytest
from django.urls import reverse

from .. import factories as f
from . import helpers

pytestmark = pytest.mark.django_db


class TestReviewerViews:
    def test_reviewer_private_comment(
        self, settings, login, conferences, create_proposal
    ):
        client = login[0]
        conference = conferences["future"]

        proposal = create_proposal

        kwargs = {"conference_slug": conference.slug, "proposal_slug": proposal.slug}
        url = reverse("proposal-comment-create", kwargs=kwargs)
        data = {"comment": "Test", "private": True}

        response = client.post(url, data)

        assert response.status_code == 302
        assert response.url.endswith("#js-reviewers")

    def test_reviewer_only_private_comment(
        self, settings, login, conferences, create_proposal
    ):
        client = login[0]
        conference = conferences["future"]

        proposal = create_proposal

        kwargs = {"conference_slug": conference.slug, "proposal_slug": proposal.slug}
        url = reverse("proposal-comment-create", kwargs=kwargs)
        data = {"comment": "Test", "reviewer": True}

        response = client.post(url, data)

        assert response.status_code == 302
        assert response.url.endswith("#js-only-reviewers")

    def test_get_review_proposal_form(
        self, settings, login, conferences, create_reviewer, create_proposal
    ):
        client = login[0]
        conference = conferences["future"]

        proposal = create_proposal

        kwargs = {"conference_slug": conference.slug, "slug": proposal.slug}
        url = reverse("proposal-review", kwargs=kwargs)

        response = client.get(url)
        context = response.context

        assert response.status_code == 200
        assert context["proposal"] == proposal
        helpers.assert_template_used(response, "proposals/review.html")

    def test_post_review_proposal(
        self, settings, login, conferences, create_reviewer, create_proposal
    ):
        client = login[0]
        conference = conferences["future"]

        proposal = create_proposal

        kwargs = {"conference_slug": conference.slug, "slug": proposal.slug}
        url = reverse("proposal-review", kwargs=kwargs)

        response = client.post(url, {"review_status": 3})

        assert response.status_code == 302

    def test_review_proposal_by_non_reviewer(
        self, settings, client, conferences, create_proposal
    ):
        username, password = "temp", "temp"
        f.create_user(password=password, username=username)
        conference = conferences["future"]
        client.login(username=username, password=password)
        proposal = create_proposal

        kwargs = {"conference_slug": conference.slug, "slug": proposal.slug}
        url = reverse("proposal-review", kwargs=kwargs)

        response = client.get(url)

        assert response.status_code == 403

    def test_proposal_reviewer_vote_by_non_reviewer(
        self, settings, client, conferences, create_proposal
    ):
        username, password = "temp", "temp"
        f.create_user(password=password, username=username)
        conference = conferences["future"]
        client.login(username=username, password=password)
        proposal = create_proposal

        kwargs = {"conference_slug": conference.slug, "proposal_slug": proposal.slug}
        url = reverse("proposal-reviewer-vote", kwargs=kwargs)

        response = client.post(url)

        assert response.status_code == 403

    def test_get_proposal_reviewer_vote(
        self, settings, login, conferences, create_proposal, create_reviewer
    ):
        client = login[0]
        conference = conferences["future"]

        proposal = create_proposal

        kwargs = {"conference_slug": conference.slug, "proposal_slug": proposal.slug}
        url = reverse("proposal-reviewer-vote", kwargs=kwargs)

        response = client.get(url)
        context = response.context

        assert response.status_code == 200
        assert context["proposal"] == proposal
        assert context["vote"] is None
        helpers.assert_template_used(response, "proposals/vote.html")

    def test_post_proposal_reviewer_vote(
        self, settings, login, conferences, create_proposal, create_reviewer
    ):
        client = login[0]
        conference = conferences["future"]

        proposal = create_proposal

        kwargs = {"conference_slug": conference.slug, "proposal_slug": proposal.slug}
        url = reverse("proposal-reviewer-vote", kwargs=kwargs)
        data = {"vote_value": 1, "comment": "Must Have"}

        response = client.post(url, data)

        assert response.status_code == 302
        assert response.url.endswith("review/") is True

    def test_update_proposal_reviewer_vote(
        self, settings, login, conferences, create_proposal, create_reviewer
    ):
        client = login[0]
        conference = conferences["future"]

        proposal = create_proposal

        kwargs = {"conference_slug": conference.slug, "proposal_slug": proposal.slug}
        url = reverse("proposal-reviewer-vote", kwargs=kwargs)
        data = {"vote_value": 1, "comment": "Must Have"}
        client.post(url, data)

        update_data = {"vote_value": 2, "comment": "Must Have"}
        response = client.post(url, update_data)

        assert response.status_code == 302
        assert response.url.endswith("review/") is True

    def test_get_proposal_reviewer_vote_after_create(
        self, settings, login, conferences, create_proposal, create_reviewer
    ):
        client = login[0]
        conference = conferences["future"]

        proposal = create_proposal

        kwargs = {"conference_slug": conference.slug, "proposal_slug": proposal.slug}
        url = reverse("proposal-reviewer-vote", kwargs=kwargs)
        comment, vote_value = "Must Have", 1
        data = {"vote_value": vote_value, "comment": comment}
        client.post(url, data)

        response = client.get(url)
        context = response.context

        assert response.status_code == 200
        assert context["form"].initial["vote_value"] == vote_value
        assert context["form"].initial["comment"] == comment

    def test_post_review_proposal_vote_with_invalid_data(
        self, settings, login, conferences, create_proposal, create_reviewer
    ):
        client = login[0]
        conference = conferences["future"]

        proposal = create_proposal

        kwargs = {"conference_slug": conference.slug, "proposal_slug": proposal.slug}
        url = reverse("proposal-reviewer-vote", kwargs=kwargs)
        data = {"vote_value": 12}
        response = client.post(url, data)

        assert response.status_code == 200
        assert "vote_value" in response.context["form_errors"]

    def test_get_proposal_votes_dashboard(self, login, conferences, create_superuser):
        client = login[0]

        conference = conferences["future"]
        kwargs = {"conference_slug": conference.slug}
        url = reverse("export-reviewer-votes", kwargs=kwargs)
        response = client.get(url)

        assert response.status_code == 200


def test_public_comment(settings, login, conferences, create_proposal):
    client = login[0]
    conference = conferences["future"]
    proposal = create_proposal

    username, password = "tmp", "tmp"
    f.create_user(password=password, username=username)
    client.login(username=username, password=password)
    kwargs = {"conference_slug": conference.slug, "proposal_slug": proposal.slug}

    url = reverse("proposal-comment-create", kwargs=kwargs)
    data = {"comment": "Test"}

    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url.endswith("#js-comments")
