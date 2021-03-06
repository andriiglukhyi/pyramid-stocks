
from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPBadRequest, HTTPServiceUnavailable, HTTPClientError
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from ..models import Stock, Account, associste
from ..models.associste import association_table
from . import DB_ERR_MSG
import requests

API_URL = ' https://api.iextrading.com/1.0'


@view_config(
    route_name='portfolio',
    renderer='../templates/portfolio.jinja2')
def entries_view(request):
    """portfolio wiwth all the stuff"""
    if request.authenticated_userid:
        if request.method == 'GET':
            """get request to portfolio page"""
            user = request.dbsession.query(Account).filter(
                    Account.username == request.authenticated_userid).first()
            return {'stock': user.stock}
    else:
        return HTTPFound(location=request.route_url('autho')) 

    if request.method == 'POST':
        """post request to portfolio page"""
        if 'symbol' not in request.POST:
            raise HTTPClientError
        symbol = request.POST['symbol']
        response = requests.get(API_URL + '/stock/{}/company'.format(symbol))
        if response.status_code == 200:
            user = request.dbsession.query(Account).filter(
                Account.username == request.authenticated_userid).first()
            query = request.dbsession.query(Stock)
            stock = query.filter(Stock.symbol == symbol).one_or_none()
            if stock is None:
                stock = Stock(**response.json())
                request.dbsession.add(stock)
            else:
                for key, value in response.json().items():
                    setattr(stock, key, value)
            stock.account.append(user)
            request.dbsession.flush()
            return HTTPFound(location=request.route_url('autho'))
        raise HTTPServiceUnavailable     


@view_config(
    route_name='stock-add',
    renderer='../templates/stock-add.jinja2')
def new_view(request):
    """add to stock view. by defaullt it's just a form for search"""
    if request.method == 'GET':
        try:
            symbol = request.GET['symbol']
        except KeyError:
            return {}
        response = requests.get(API_URL + '/stock/{}/company'.format(symbol))
        data = response.json()
        return {'company': data,
                'responce': 200}


@view_config(
    route_name='stock-details',
    renderer='../templates/stock-details.jinja2',
    request_method='GET')
def detail_view(request):
    """details about single item"""
    if request.authenticated_userid:
        try:
            entry_id = request.matchdict['symbol']
        except KeyError:
            return HTTPNotFound()
        try:
            query = request.dbsession.query(Stock)
            entry_detail = query.filter(Stock.symbol == entry_id).one_or_none()
            if entry_detail is None:
                return HTTPNotFound('Sorry')
            for item in entry_detail.account:
                if item.username == request.authenticated_userid:
                    return {"lst": entry_detail}
        except DBAPIError:
            return Response(DB_ERR_MSG, content_type='text/plain', status=500)

    else:
        return HTTPFound(location=request.route_url('home'))