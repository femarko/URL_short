from datetime import datetime

from sqlalchemy import text

from src.shortener_app.domain.models import URLShortened
from src.shortener_app.repository.repository import URLRepository
from src.shortener_app.orm_tool.sql_aclchemy_wrapper import orm_conf


async def test_repository_can_save_the_urls(reset_db_fixture):
    # orm_conf.start_mapping()
    # await orm_conf.reset_db()
    fake_original_url, fake_short_url = "fake_original_url", "fake_short_url"
    session = orm_conf.session_maker
    async with session() as session:
        repo = URLRepository(session=session)
        await repo.add(URLShortened(original_url=fake_original_url, short_url=fake_short_url))
        await session.commit()
    sess = orm_conf.session_maker
    async with sess() as sess:
        result = await sess.execute(text(f"SELECT * FROM url_shortened WHERE original_url='{fake_original_url}'"))
        data_from_db = result.fetchall()[0]
    # await orm_conf.reset_db()
    assert data_from_db[0] == 1
    assert data_from_db[1] == "fake_original_url"
    assert data_from_db[2] == "fake_short_url"
    assert (data_from_db[3]).isoformat().startswith(str(datetime.date(datetime.now())))


async def test_repository_can_get_the_urls():
    fake_original_url, fake_short_url = "fake_original_url", "fake_short_url"
    session = orm_conf.session_maker
    async with session() as session:
        repo = URLRepository(session=session)
        await repo.add(URLShortened(original_url=fake_original_url, short_url=fake_short_url))
        await session.commit()
        result = await repo.get(instance_id=1)
    await orm_conf.reset_db()
    assert result.id == 1
    assert result.original_url == "fake_original_url"
    assert result.short_url == "fake_short_url"
    assert result.save_date.date() == datetime.date(datetime.now())


async def test_repository_can_delete_the_urls():
    fake_original_url, fake_short_url = "fake_original_url", "fake_short_url"
    session = orm_conf.session_maker
    async with session() as session:
        repo = URLRepository(session=session)
        await repo.add(URLShortened(original_url=fake_original_url, short_url=fake_short_url))
        await session.commit()
        instance = await repo.get(instance_id=1)
    sess = orm_conf.session_maker
    async with sess() as session:
        repo = URLRepository(session=session)
        await repo.delete(instance=instance)
        await session.commit()
        result = await repo.get(instance_id=1)
    assert result is None
