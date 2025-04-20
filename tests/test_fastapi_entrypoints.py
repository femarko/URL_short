import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_cut_url(async_client, reset_db_fixture):
    response_1 = await async_client.post(url="/", json={"url": "https://google.com"})
    response_json_1 = response_1.json()
    response_2 = await async_client.post(url="/", json={"url": "https://google.com"})
    assert response_1.status_code == 201
    assert response_2.status_code == 200
    assert "short_url" in response_json_1
    assert isinstance(response_json_1["short_url"], str)
    assert response_json_1["short_url"].startswith("https://tinyurl.com/")
    assert "id" in response_json_1
    assert isinstance(response_json_1["id"], int)
    assert response_2.json() == response_json_1


@pytest.mark.asyncio(loop_scope="session")
async def test_get_original_url(async_client, reset_db_fixture):
    await async_client.post(url="/", json={"url": "https://google.com"})
    response = await async_client.get(url="/1", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["Location"] == "https://google.com/"
