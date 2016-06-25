# Third Party Stuff
import pytest
from tests import factories as f


@pytest.mark.parametrize('method', [
    'get_absolute_url',
    'get_delete_url',
    'get_down_vote_url',
    'get_hashid',
    'get_remove_vote_url',
    'get_review_url',
    'get_slug',
    'get_up_vote_url',
    'get_update_url',
    'get_vote_url',
    '__str__',
])
def test_proposal_model_method_works(db, method):
    proposal = f.ProposalFactory()
    assert getattr(proposal, method)()
