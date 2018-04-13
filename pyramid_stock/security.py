import os
from pyramid.security import Allow, Everyone, Authenticated
from pyramid.session import SignedCookieSessionFactory
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy


class MyRoot:
    def __init__(self, request):
        self.request = request

    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Everyone, 'secret'),
    ]


def includeme(config):
    """insclude for include"""
    auth_secret = os.environ.get('AUTH_SECRET', 'itsasecret')
    authz_policy = ACLAuthorizationPolicy()
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512',
    )

    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.set_default_permission('secret')
    config.set_root_factory(MyRoot)

    session_secret = os.environ.get('SESSION_SECRET', 'itsalsoaseekret')
    session_factory = SignedCookieSessionFactory(session_secret)

    config.set_session_factory(session_factory)
    config.set_default_csrf_options(require_csrf=True)
    