from .. import factories as f


def test_conferences(client, db):
    conference = f.ConferenceFactory()
    response = client.get('/')
    assert str(conference.name) in str(response.content)

    # should not display the conference if it's set as deleted
    conference.deleted = True
    conference.save()
    response = client.get('/')
    assert str(conference.name) not in str(response.content)
