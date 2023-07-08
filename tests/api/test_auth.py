import pytest


@pytest.mark.asyncio
async def test_auth_me(client, resetdb, user):
    response = await client.get("/api/v1/auth/me")

    assert response.status_code == 200
    assert response.json()['data']['me'] == user['user']


@pytest.mark.asyncio
async def test_logout(client, resetdb, user):
    response = await client.post('/api/v1/auth/logout')

    assert response.status_code == 200
    assert response.json()['data']['me']['id'] != user['user']['id']
