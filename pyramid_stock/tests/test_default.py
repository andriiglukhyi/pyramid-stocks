def test_default_behavior_of_base_view(dummy_request):
    """test base view status and type"""
    from ..views.default import home_view
    request = dummy_request
    response = home_view(request)
    assert response['status'] == 200
    assert response['text'] == 'OK'
    assert type(response) == dict


def test_default_response_home_view(dummy_request):
    """test home view"""
    from ..views.default import home_view
    response = home_view(dummy_request)
    assert len(response) == 2
    assert type(response) == dict


def test_default_response_auth_view(dummy_request):
    """test auth view"""
    from ..views.entry import entries_view
    response = entries_view(dummy_request)
    assert type(response) == dict


def test_auth_signin_view(dummy_request):
    """test auth_view with empty username"""
    from ..views.auth import auth_view
    dummy_request.GET = {'username': ''}
    response = auth_view(dummy_request)
    assert response['status_code'] == 302
    assert type(response) == dict


def test_auth_signup_view(dummy_request):
    """test signup view"""
    from ..views.auth import auth_view
    dummy_request.POST = {'username': 'watman', 'password': 'whodat', 'email': 'wat@wat.com'}
    dummy_request.method = 'POST'
    response = auth_view(dummy_request)
    assert response.status_code == 302
    from pyramid.httpexceptions import HTTPFound
    assert isinstance(response, HTTPFound)


def test_bad_reqeust_auth_signup_view(dummy_request):
    """test auth_view with brocken POST req"""
    from ..views.auth import auth_view
    from pyramid.httpexceptions import HTTPBadRequest
    dummy_request.POST = {'password': 'whodat', 'email': 'wat@wat.com'}
    dummy_request.method = 'POST'
    response = auth_view(dummy_request)
    assert response.status_code == 400
    assert isinstance(response, HTTPBadRequest)


def test_bad_request_method_auth_signup_view(dummy_request):
    """test post reques with correct params"""
    from ..views.auth import auth_view
    from pyramid.httpexceptions import HTTPFound
    dummy_request.POST = {'password': 'whodat', 'email': 'wat@wat.com'}
    dummy_request.method = 'PUT'
    response = auth_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_bad_reqeust_auth_logout_view_(dummy_request):
    """test logout"""
    from ..views.auth import logout
    response = logout(dummy_request)
    from pyramid.httpexceptions import HTTPFound
    assert isinstance(response, HTTPFound)

def test_bad_reqeust_auth_signup_POst___(dummy_request, db_session):
    """test signup view"""
    from ..models import Stock
    from ..views.auth import auth_view
    assert len(db_session.query(Stock).all()) == 0
    dummy_request.POST = {'username': 'watman', 'password': 'whodat', 'email': 'wat@wat.com'}
    dummy_request.method = 'POST'
    entry = Stock(symbol='symbol')
    db_session.add(entry)
    response = auth_view(dummy_request)
    from pyramid.httpexceptions import HTTPFound
    assert isinstance(response, HTTPFound)


def test_default_response_entries_view_bad_db(dummy_request):
    """test new_wiev"""
    from ..views.entry import new_view
    dummy_request.GET = {'s': 'dsd'}
    response = new_view(dummy_request)
    assert response == {}


def test_default_stock_details_(dummy_request, db_session):
    """test query db with incorrect key"""
    from ..views.entry import detail_view
    dummy_request.GET = {'sdcs': 'ss'}
    response = detail_view(dummy_request)
    from pyramid.httpexceptions import HTTPNotFound
    assert isinstance(response, HTTPNotFound)


def test_default_notfound__(dummy_request):
    """test 404_wiev"""
    from ..views.notfound import notfound_view
    response = notfound_view(dummy_request)
    assert response == {}
    
def test_semple_data_():
    """test datA"""
    from ..sample_data.__init__ import MOCK_DATA
    assert type(MOCK_DATA) == list

def test_default_stock_details__(dummy_request, db_session):
    """test detail view KeyError"""
    from ..views.entry import detail_view
    dummy_request.GET = {'dfs': 'ss'}
    response = detail_view(dummy_request)
    from pyramid.httpexceptions import HTTPNotFound
    assert isinstance(response, HTTPNotFound)





