# -*- coding: utf-8 -*-

from django.urls import reverse

from .. import factories as f


def test_conferences(client, db):
    conference = f.ConferenceFactory()
    response = client.get("/")
    assert str(conference.name) in str(response.content)

    # should not display the conference if it's set as deleted
    conference.deleted = True
    conference.save()
    response = client.get("/")
    assert str(conference.name) not in str(response.content)


def test_get_conference_found(client, db):
    conference = f.ConferenceFactory()
    url = reverse("get-conference", kwargs={"conference_slug": conference.slug})
    response = client.get(url, follow=True)
    assert response.redirect_chain == [
        (reverse("proposals-list", kwargs={"conference_slug": conference.slug}), 302)
    ]
    assert str(conference.name) in str(response.content)


def test_conference_not_found(client, db):
    url = reverse(
        "get-conference", kwargs={"conference_slug": "non-existent-conference"}
    )
    response = client.get(url, follow=True)
    assert len(response.redirect_chain) == 0
    assert response.status_code == 404
