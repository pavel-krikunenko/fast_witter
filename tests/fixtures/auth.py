import random
from string import ascii_letters

import pytest


@pytest.fixture(scope="module")
async def user(
        resetdb,
        client
) -> dict:
    response = await client.post(
        "/api/v1/auth/sign-up",
        json={
            'name': "".join([random.choice(ascii_letters) for i in range(10)]),
            "password": "password"
        }
    )
    assert response.status_code == 200
    return {
        "token": response.json()['data']['token'],
        "user": response.json()['data']['me']
    }
