# -*- coding: utf-8 -*-

import pytest
from django.urls import reverse

from .. import factories as f
from . import helpers

pytestmark = pytest.mark.django_db


#  Proposal
def test_list_proposals_pass(client, settings):
    conference = f.create_conference()
    url = reverse("proposals-list", kwargs={"conference_slug": conference.slug})
    response = client.get(url)

    assert response.status_code == 200


def test_list_proposals_fail(client, settings):
    url = reverse("proposals-list", kwargs={"conference_slug": "conf-404"})
    response = client.get(url)

    assert response.status_code == 404


def test_create_proposal_for_closed_conference(settings, login, conferences):
    client = login[0]
    conference = conferences["past"]
    url = reverse("proposal-create", kwargs={"conference_slug": conference.slug})
    response = client.get(url)
    template = "proposals/closed.html"

    assert response.status_code == 200
    helpers.assert_template_used(response=response, template_name=template)


def test_create_proposal_for_open_conference_get(settings, login, conferences):
    client = login[0]
    conference = conferences["future"]
    url = reverse("proposal-create", kwargs={"conference_slug": conference.slug})
    response = client.get(url)
    template = "proposals/create.html"

    assert response.status_code == 200
    helpers.assert_template_used(response=response, template_name=template)
    assert response.context["conference"] == conference


def test_create_proposal_with_missing_data(settings, login, conferences):
    client = login[0]
    conference = conferences["future"]
    url = reverse("proposal-create", kwargs={"conference_slug": conference.slug})

    data = {
        "title": "Proposal Title for the conf",
        "description": "Loong Text",
        "target_audience": "1",
        "status": "2",
        "proposal_type": 34,
        "proposal_section": 34,
    }
    response = client.post(url, data)

    assert response.status_code == 200
    assert set(response.context["errors"].keys()) == set(
        ["proposal_type", "proposal_section"]
    )


def test_create_proposal_with_all_data(settings, login, conferences):
    client = login[0]
    conference = conferences["future"]
    url = reverse("proposal-create", kwargs={"conference_slug": conference.slug})
    section = conference.proposal_sections.all()[0]
    proposal_type = conference.proposal_types.all()[0]

    data = {
        "title": "Proposal Title for the conf",
        "description": "Loong Text",
        "target_audience": "1",
        "status": "2",
        "proposal_type": proposal_type.id,
        "proposal_section": section.id,
    }
    response = client.post(url, data)

    assert response.status_code == 302


def test_delete_existing_proposal_post(settings, login, conferences):
    client, user = login[0], login[1]
    conference = conferences["future"]
    section = conference.proposal_sections.all()[0]
    proposal_type = conference.proposal_types.all()[0]
    proposal = f.create_proposal(
        conference=conference,
        proposal_section=section,
        proposal_type=proposal_type,
        author=user,
    )
    kwargs = {"conference_slug": conference.slug, "slug": proposal.slug}
    url = reverse("proposal-delete", kwargs=kwargs)

    response = client.post(url)

    assert response.status_code == 302


def test_delete_existing_proposal_get(settings, login, conferences):
    client, user = login[0], login[1]
    conference = conferences["future"]
    section = conference.proposal_sections.all()[0]
    proposal_type = conference.proposal_types.all()[0]
    proposal = f.create_proposal(
        conference=conference,
        proposal_section=section,
        proposal_type=proposal_type,
        author=user,
    )
    kwargs = {"conference_slug": conference.slug, "slug": proposal.slug}
    url = reverse("proposal-delete", kwargs=kwargs)

    response = client.get(url)

    assert response.status_code == 200
    helpers.assert_template_used(response, "proposals/delete.html")


def test_delete_existing_proposal_by_different_author(settings, login, conferences):
    client = login[0]
    conference = conferences["future"]
    section = conference.proposal_sections.all()[0]
    proposal_type = conference.proposal_types.all()[0]
    user = f.create_user()
    proposal = f.create_proposal(
        conference=conference,
        proposal_section=section,
        proposal_type=proposal_type,
        author=user,
    )
    kwargs = {"conference_slug": conference.slug, "slug": proposal.slug}
    url = reverse("proposal-delete", kwargs=kwargs)

    response = client.post(url)

    assert response.status_code == 403


def test_update_proposal_get(settings, login, conferences):
    client, user = login[0], login[1]
    conference = conferences["future"]
    section = conference.proposal_sections.all()[0]
    proposal_type = conference.proposal_types.all()[0]
    proposal = f.create_proposal(
        conference=conference,
        proposal_section=section,
        proposal_type=proposal_type,
        author=user,
    )
    kwargs = {"conference_slug": conference.slug, "slug": proposal.slug}
    url = reverse("proposal-update", kwargs=kwargs)

    response = client.get(url)

    assert response.status_code == 200
    helpers.assert_template_used(response, "proposals/update.html")
    assert response.context["proposal"] == proposal


def test_update_proposal_post(settings, login, conferences):
    client, user = login[0], login[1]
    conference = conferences["future"]
    section = conference.proposal_sections.all()[0]
    proposal_type = conference.proposal_types.all()[0]
    proposal = f.create_proposal(
        conference=conference,
        proposal_section=section,
        proposal_type=proposal_type,
        author=user,
    )
    kwargs = {"conference_slug": conference.slug, "slug": proposal.slug}
    url = reverse("proposal-update", kwargs=kwargs)

    title = "new proposal title"
    data = {
        "title": title,
        "description": "Loong Text",
        "target_audience": "1",
        "status": "2",
        "proposal_type": proposal_type.id,
        "proposal_section": section.id,
    }

    response = client.post(url, data)

    assert response.status_code == 302


def test_update_proposal_by_different_user(settings, login, conferences):
    client = login[0]
    conference = conferences["future"]
    section = conference.proposal_sections.all()[0]
    proposal_type = conference.proposal_types.all()[0]
    user = f.create_user()
    proposal = f.create_proposal(
        conference=conference,
        proposal_section=section,
        proposal_type=proposal_type,
        author=user,
    )

    kwargs = {"conference_slug": conference.slug, "slug": proposal.slug}
    url = reverse("proposal-update", kwargs=kwargs)
    title = "new proposal title"
    data = {"title": title}
    response = client.post(url, data)

    assert response.status_code == 403


def test_update_proposal_with_invalid_data(settings, login, conferences):
    client, user = login[0], login[1]
    conference = conferences["future"]
    section = conference.proposal_sections.all()[0]
    proposal_type = conference.proposal_types.all()[0]
    proposal = f.create_proposal(
        conference=conference,
        proposal_section=section,
        proposal_type=proposal_type,
        author=user,
    )
    kwargs = {"conference_slug": conference.slug, "slug": proposal.slug}
    url = reverse("proposal-update", kwargs=kwargs)

    title = "new title"
    response = client.post(url, {"title": title})

    assert response.status_code == 200
    assert "title" in response.context["errors"]


def test_proposal_filters(settings, login, conferences):
    client, user = login[0], login[1]
    conference = conferences["future"]
    section = conference.proposal_sections.all()[1]
    proposal_type = conference.proposal_types.all()[1]
    f.create_proposal(
        conference=conference,
        proposal_section=section,
        proposal_type=proposal_type,
        author=user,
    )
    kwargs = {"conference_slug": conference.slug}
    url = reverse("proposals-list", kwargs=kwargs)

    response = client.get(
        url, {"proposal_section": section.id, "proposal_type": proposal_type.id}
    )

    assert response.status_code == 200
    assert response.context["is_filtered"] is True


def test_proposal_detail_url_redirects(client):
    proposal = f.create_proposal()
    old_url = reverse(
        "proposal-detail",
        kwargs={
            "conference_slug": proposal.conference.slug,
            "slug": proposal.get_slug(),
        },
    )
    response = client.get(old_url)
    assert response.status_code == 302
    assert proposal.get_absolute_url() in response["Location"]

    # should redirect the wrong slug, having correct hashid
    url = reverse(
        "proposal-detail",
        kwargs={
            "conference_slug": proposal.conference.slug,
            "slug": "bla-bla-bla",
            "hashid": proposal.get_hashid(),
        },
    )
    response = client.get(url)
    assert response.status_code == 302
    assert proposal.get_absolute_url() in response["Location"]
