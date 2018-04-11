from datetime import datetime


def test_constructed_entry_with_correct_date_added_to_database(db_session):
    """test db add 1 iteem in"""
    from ..models import Stock
    assert len(db_session.query(Stock).all()) == 0
    entry = Stock(symbol='symbol')
    db_session.add(entry)
    assert len(db_session.query(Stock).all()) == 1


def test_constructed_entry_with_no_date_added_to_database(db_session):
    """test db with one symbol"""
    from ..models import Stock
    assert len(db_session.query(Stock).all()) == 0
    entry = Stock(symbol='fake symbol', exchange='New York Stock Exchange')
    db_session.add(entry)
    assert len(db_session.query(Stock).all()) == 1


def test_constructed_entry_with_date_added_to_database(db_session):
    """test db add a cople fields"""
    from ..models import Stock
    assert len(db_session.query(Stock).all()) == 0
    entry = Stock(
        symbol='new_symbol',
        CEO='CEO')
    db_session.add(entry)
    assert len(db_session.query(Stock).all()) == 1


def test_entry_with_no_title_throws_error(db_session):
    """test query empty db"""
    from ..models import Stock
    assert len(db_session.query(Stock).all()) == 0