import pytest
from async_asgi_testclient import TestClient


@pytest.mark.asyncio
async def test_create_post(client, resetdb, user, post):
    ...


@pytest.mark.parametrize(
    "title,body",
    [
        ("new_title1", 'new_body1'),
        (None, 'new_body2'),
        ("new_title2", None),
        (None, None)
    ])
@pytest.mark.asyncio
async def test_update_post(client: TestClient, resetdb, user, post, title, body):
    data = {}
    if title:
        data['title'] = title
    if body:
        data['body'] = body

    response = await client.post(
        f"/api/v1/posts/{post['id']}",
        json=data
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_post(client: TestClient, resetdb, user, post):
    response = await client.delete(f"/api/v1/posts/{post['id']}")

    assert response.status_code == 200


@pytest.mark.parametrize('page, limit', [(1, 10), (2, 10)])
@pytest.mark.asyncio
async def test_get_list_posts(
        client: TestClient,
        resetdb,
        user,
        post,
        page,
        limit
):
    response = await client.get(
        f'/api/v1/posts/?{page=}&{limit=}'
    )
    assert response.status_code == 200
    assert response.json()['data']['limit'] == limit
    assert response.json()['data']['page'] == page


@pytest.mark.asyncio
async def test_post_like(
        client: TestClient,
        resetdb,
        user,
        post
):
    response1 = await client.get(
        f"/api/v1/posts/{post['id']}/like"
    )
    assert response1.status_code == 200
    assert user['user']['id'] in response1.json()['data']['likes']

    response2 = await client.get(
        f"/api/v1/posts/{post['id']}/like"
    )
    assert response2.status_code == 200
    assert user['user']['id'] not in response2.json()['data']['likes']
