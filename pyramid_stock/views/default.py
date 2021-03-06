from pyramid.view import view_config
from pyramid.security import NO_PERMISSION_REQUIRED


@view_config(
    route_name='home',
    renderer='../templates/base.jinja2',
    request_method='GET',
    permission=NO_PERMISSION_REQUIRED)
def home_view(request):
    return {'text': 'OK',
            'status': 200}