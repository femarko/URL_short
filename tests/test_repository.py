from datetime import datetime

from sqlalchemy import text

from src.shortener_app.domain.models import URLShortened
from src.shortener_app.repository.repository import URLRepository
from src.shortener_app.orm_tool.sql_aclchemy_wrapper import orm_conf


def test_repository_can_save_the_urls():
    fake_original_url, fake_short_url = "fake_original_url", "fake_short_url"
    session = orm_conf.session_maker
    with session() as session:
        repo = URLRepository(session=session)
        repo.add(URLShortened(original_url=fake_original_url, short_url=fake_short_url))
        session.commit()
    sess = orm_conf.session_maker
    with sess() as sess:
        result = sess.execute(text(f"SELECT * FROM url_shortened WHERE original_url='{fake_original_url}'"))
        data_from_db = result.fetchall()[0]
    assert data_from_db[0] == 1
    assert data_from_db[1] == "fake_original_url"
    assert data_from_db[2] == "fake_short_url"
    assert data_from_db[3].startswith(str(datetime.date(datetime.now())))


def test_repository_can_get_the_urls():
    fake_original_url, fake_short_url = "fake_original_url", "fake_short_url"
    session = orm_conf.session_maker
    with session() as session:
        repo = URLRepository(session=session)
        repo.add(URLShortened(original_url=fake_original_url, short_url=fake_short_url))
        session.commit()
        result = repo.get(instance_id=1)
    assert result.id == 1
    assert result.original_url == "fake_original_url"
    assert result.short_url == "fake_short_url"
    assert result.save_date.date() == datetime.date(datetime.now())


def test_repository_can_delete_the_urls():
    fake_original_url, fake_short_url = "fake_original_url", "fake_short_url"
    session = orm_conf.session_maker
    with session() as session:
        repo = URLRepository(session=session)
        repo.add(URLShortened(original_url=fake_original_url, short_url=fake_short_url))
        session.commit()
        instance = repo.get(instance_id=1)
    sess = orm_conf.session_maker
    with sess() as session:
        repo = URLRepository(session=session)
        repo.delete(instance=instance)
        session.commit()
        result = repo.get(instance_id=1)
    assert result is None
