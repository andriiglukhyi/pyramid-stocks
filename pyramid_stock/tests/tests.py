
def test_default_behavior_of_base_view(dummy_request):
    from ..views.default import home_view
    request = dummy_request
    response = home_view(request)
    assert response['status'] == 200
    assert response['text'] == 'OK'
    assert type(response) == dict

 
def test_default_behavior_of_auth_view(dummy_request):
    from ..views.default import auth_view
    response = auth_view(dummy_request)
    assert type(response) == dict
    assert response == {}
    response.values == 0


def test_default_entries_view(dummy_request):
    from ..views.default import entries_view
    response = entries_view(dummy_request)
    assert type(response) == dict
    assert response['stock'][0]['CEO'] == 'John L. Flannery'


def test_new_view_default(dummy_request):
    from ..views.default import new_view
    response = new_view(dummy_request)
    assert type(response) == dict


def test_default_view(dummy_request):
    from ..views.default import detail_view
    response = detail_view(dummy_request)
    assert type(response) == dict


 
