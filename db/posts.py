import logging
from typing import Optional

from misc import db
from models import posts

logger = logging.getLogger(__name__)

TABLE = "posts"


async def create_post(
        conn: db.Connection,
        user_id: int,
        new_post: posts.NewPost
) -> Optional[posts.Post]:
    return db.record_to_model(
        posts.Post,
        await db.create(
            conn=conn,
            table=TABLE,
            data={
                "author_id": user_id,
                "title": new_post.title,
                "body": new_post.body
            }
        )
    )


async def update_post(
        conn: db.Connection,
        post_id: int,
        update_model: posts.UpdatePost
) -> Optional[posts.Post]:
    return db.record_to_model(
        posts.Post,
        await db.update(
            conn=conn,
            table=TABLE,
            pk=post_id,
            data=update_model.dict(exclude_none=True)
        )
    )


async def get_post(
        conn: db.Connection,
        post_id: int
) -> Optional[posts.Post]:
    return db.record_to_model(
        posts.Post,
        await db.get(
            conn=conn,
            table=TABLE,
            pk=post_id
        )
    )


async def get_posts_list(
        conn: db.Connection,
        page: int,
        limit: int
) -> list[posts.Post]:
    return db.record_to_model_list(
        posts.Post,
        await db.get_list(
            conn=conn,
            table=TABLE,
            limit=limit,
            offset=limit * (page - 1),
            where=""
        )
    )


async def get_total(
        conn: db.Connection,
) -> int:
    return (await db.get_total(conn, TABLE)).get('count', 0)


async def delete_post(
        conn: db.Connection,
        post_id: int
) -> Optional[posts.Post]:
    return db.record_to_model(
        posts.Post,
        await db.delete_by_where(
            conn=conn,
            pk=post_id,
            table=TABLE
        )
    )
