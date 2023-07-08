from typing import Optional

from misc import db
from models import users

TABLE = 'users'


async def create_user(
        conn: db.Connection,
        name: str,
        password: str
) -> Optional[users.User]:
    return db.record_to_model(
        users.User,
        await db.create(
            conn=conn,
            table=TABLE,
            data={
                'name': name,
                "pass_hash": password
            }
        )
    )


async def get_user_by_creds(
        conn: db.Connection,
        name: str,
        password: str
) -> Optional[users.User]:
    return db.record_to_model(
        users.User,
        await db.get_by_where(
            conn=conn,
            table=TABLE,
            where=" name = $1 and pass_hash = $2",
            values=[name, password]
        )
    )


async def get_user_by_name(
        conn: db.Connection,
        name: str
) -> Optional[users.User]:
    return db.record_to_model(
        users.User,
        await db.get_by_where(
            conn=conn,
            table=TABLE,
            where=" name = $1 ",
            values=[name]
        )
    )

async def get_user(
        conn: db.Connection,
        pk: int
) -> users.User:
    return db.record_to_model(
        users.User,
        await db.get(
            conn=conn,
            table=TABLE,
            pk=pk
        )
    )
