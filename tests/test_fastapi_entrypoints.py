from fastapi.testclient import TestClient

from src.shortener_app.entrypoints.fastapi_app.main import app
from src.shortener_app.orm_tool.sql_aclchemy_wrapper import orm_conf
from src.shortener_app.domain.models import URLShortened

def test_cut_url(client):
    response_1 = client.post(url="/", json={"url": "https://google.com"})
    response_json_1 = response_1.json()
    response_2 = client.post(url="/", json={"url": "https://google.com"})
    assert response_1.status_code == 201
    assert response_2.status_code == 200
    assert "short_url" in response_json_1
    assert isinstance(response_json_1["short_url"], str)
    assert response_json_1["short_url"].startswith("https://tinyurl.com/")
    assert "id" in response_json_1
    assert isinstance(response_json_1["id"], int)
    assert response_2.json() == response_json_1


def test_get_original_url(client):
    response = client.get(url="/1", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["Location"] == "https://google.com/"
