def test_default_behavior_of_base_view(dummy_request):
    from ..views.default import home
    from pyramid.response import Response
    request = dummy_request
    response = home(request)
    assert isinstance(response, Response)
    assert response.text['status'] == '200'


def test_default_behavior_of_entries_view(dummy_request):
    from ..views.default import portfolio
    response = portfolio(dummy_request)
    assert type(response) == dict
    assert response['entries'][0]['id'] == "AE"


