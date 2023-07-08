import pytest


@pytest.fixture(scope='function')
async def post(client, resetdb, user):
    response = await client.post(
        "/api/v1/posts/",
        json={
            "title": "test_title",
            "body": "test_body"
        }
    )

    assert response.status_code == 200
    assert response.json()['data']['title'] == 'test_title'
    assert response.json()['data']['body'] == 'test_body'
    return response.json()['data']
