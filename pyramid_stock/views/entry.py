
from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPBadRequest
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from ..models import Stock
from . import DB_ERR_MSG
import requests
import os

API_URL = ' https://api.iextrading.com/1.0'


@view_config(
    route_name='portfolio',
    renderer='../templates/portfolio.jinja2')
def entries_view(request):
    """portfolio wiwth all the stuff"""
    if request.method == 'GET':
        """get request to portfolio page"""
        try:
            query = request.dbsession.query(Stock)
            all_entries = query.all()
        except DBAPIError:
            return DBAPIError(DB_ERR_MSG, content_type='text/plain', status=500)

        return {'stock': all_entries}

    if request.method == 'POST':
        """post request to portfolio page"""
        symbol = request.POST['symbol']
        response = requests.get(API_URL + '/stock/{}/company'.format(symbol))
        if response.status_code == 200:
            try:
                query = request.dbsession.query(Stock)
                stock = query.filter(Stock.symbol == symbol).one_or_none()
            except DBAPIError:
                return DBAPIError(
                    DB_ERR_MSG, content_type='text/plain', status=500)
            if stock is None:
                request.dbsession.add(Stock(**response.json()))
            else:
                for key, value in response.json().items():
                    setattr(stock, key, value)
        query = request.dbsession.query(Stock)
        all_entries = query.all()
        return {'stock': all_entries}


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
    try:
        entry_id = request.matchdict['symbol']
    except KeyError:
        return HTTPNotFound()

    try:
        query = request.dbsession.query(Stock)
        entry_detail = query.filter(Stock.symbol == entry_id).one_or_none()
    except DBAPIError:
        return DBAPIError(DB_ERR_MSG, content_type='text/plain', status=500)
    if entry_detail is None:
        response = requests.get(API_URL + '/stock/{}/company'.format(entry_id))
        data = response.json()
        return {"lst": data}
    return {"lst": entry_detail}