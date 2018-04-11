import pytest
from pyramid import testing
from ..models.meta import Base
from ..models import Stock
from sqlalchemy.exc import DBAPIError
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest, HTTPUnauthorized, HTTPNotFound



@pytest.fixture
def test_stock():
    """fixture for DB"""
    return Stock(
        symbol='fake symbol',
        companyName='fake companyName',
        exchange='New York Stock Exchange',
        industry='industry',
        website='website',
        description='description',
        CEO='CEO',
        issueType='issueType',
        sector='sector'
    )


@pytest.fixture
def configuration(request):
    """Setup a database for testing purposes."""
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://postgres:postgres@localhost:5432/prod'
    })
    config.include('pyramid_stock.models')
    config.include('pyramid_stock.routes')

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """Create a database session for interacting with the test database."""
    SessionFactory = configuration.registry['dbsession_factory']
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Create a dummy GET request with a dbsession."""
    return testing.DummyRequest(dbsession=db_session)