from pyramid.view import view_config
from pyramid.response import Response
from ..sample_data import MOCK_DATA
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
import requests

API_URL = ' https://api.iextrading.com/1.0'


@view_config(
    route_name='home',
    renderer='../templates/base.jinja2',
    request_method='GET')
def home_view(request):
    return {'text': 'OK',
            'status': 200}


@view_config(
    route_name='autho',
    renderer='../templates/autho.jinja2')
def auth_view(request):
    if request.method == 'GET':
        try:
            username = request.GET['username']
            password = request.GET['password']
            print('User: {}, Pass: {}'.format(username, password))

            return HTTPFound(location=request.route_url('home'))

        except KeyError:
            return {}

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        print('User: {}, Pass: {}, Email: {}'.format(username, password, email))

        return HTTPFound(location=request.route_url('portfolio'))

    return HTTPNotFound()


@view_config(
    route_name='portfolio',
    renderer='../templates/portfolio.jinja2')
def entries_view(request):
    if request.method == 'GET':
        return {'stock': MOCK_DATA}
    if request.method == 'POST':
        symbol = request.POST['symbol']
        response = requests.get(API_URL + '/stock/{}/company'.format(symbol))
        data = response.json()
        MOCK_DATA.append(data)
        return {'stock': MOCK_DATA}


@view_config(
    route_name='stock-add',
    renderer='../templates/stock-add.jinja2',
    request_method='GET')
def new_view(request):
    if request.method == 'GET':
        try:
            symbol = request.GET['symbol']
        except KeyError:
            return {}
        response = requests.get(API_URL + '/stock/{}/company'.format(symbol))
        data = response.json()
        return {'company': data}


@view_config(
    route_name='stock-details',
    renderer='../templates/stock-details.jinja2',
    request_method='GET')
def detail_view(request):
    try:
        que = request.matchdict['symbol']
        for item in MOCK_DATA:
            if item['symbol'] == que:
                return {'lst': item}
        
    except KeyError:
        return {}