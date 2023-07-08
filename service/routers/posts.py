import logging

from fastapi import APIRouter, Depends

from db import posts
from misc import redis
from misc.db import Connection
from misc.depends.db import get as get_conn
from misc.depends.redis import get as get_redis
from misc.depends.session import get as get_session
from misc.handlers import (
    UnauthenticatedException,
    error_500, error_404, error_403
)
from misc.session import Session
from models import posts as posts_models
from models.base import SuccessResponse

logger = logging.getLogger(__name__)


async def check_auth(
        session: Session = Depends(get_session)
):
    if not session.user.is_authenticated:
        raise UnauthenticatedException
    return


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    dependencies=[Depends(check_auth)]
)


@router.post("/", response_model=posts_models.PostSuccessResponse)
async def create_post(
        model: posts_models.NewPost,
        conn: Connection = Depends(get_conn),
        session: Session = Depends(get_session),
        cache: redis.Redis = Depends(get_redis)
):
    """
    Create post

    """
    if not (new_post := await posts.create_post(
            conn=conn,
            user_id=session.session_user_id,
            new_post=model
    )):
        return await error_500()
    await redis.set(
        f"post_{new_post.id}",
        value={
            "likes": []
        },
        conn=cache
    )
    return posts_models.PostSuccessResponse(
        data=new_post
    )


@router.get("/", response_model=posts_models.PostsListSuccessResponse)
async def get_posts(
        page: int = 1,
        limit: int = 20,
        conn: Connection = Depends(get_conn),
        cache: redis.Redis = Depends(get_redis)
):
    """
    posts list with pagination\n

    """

    limit = max(min(20, limit), 1)
    page = max(page, 1)

    return posts_models.PostsListSuccessResponse(
        data=posts_models.PostsListData(
            items=[
                await add_post_likes_to_model(cache, i)
                for i
                in await posts.get_posts_list(
                    conn,
                    page,
                    limit
                )
            ],
            limit=limit,
            page=page,
            total=await posts.get_total(conn)
        )
    )


@router.post("/{post_id}", response_model=posts_models.PostSuccessResponse)
async def update_post(
        post_id: int,
        update_model: posts_models.UpdatePost,
        conn: Connection = Depends(get_conn),
        session: Session = Depends(get_session)
):
    """
    update post\n
    model fields are optional\n

    if post not found return 404\n
    if post.author not equal current user return 403\n
    else return updated post\n

    """
    if not (post := await posts.get_post(conn, post_id)):
        return await error_404()
    if post.author_id != session.session_user_id:
        return await error_403()
    if update_model.body is None and update_model.title is None:
        return posts_models.PostSuccessResponse(
            data=post
        )
    return posts_models.PostSuccessResponse(
        data=await posts.update_post(conn, post_id, update_model)
    )


@router.delete("/{post_id}", response_model=SuccessResponse)
async def delete_post(
        post_id: int,
        conn: Connection = Depends(get_conn),
        session: Session = Depends(get_session)
):
    """
    Post delete.\n
    if post not found return 404\n
    if post.author not equal current user return 403\n
    if delete returns None, endpoint returns 500\n

    """

    if not (post := await posts.get_post(conn, post_id)):
        return await error_404()
    if post.author_id != session.session_user_id:
        return await error_403()
    if not await posts.delete_post(
            conn=conn,
            post_id=post_id
    ):
        return error_500()
    return SuccessResponse()


@router.get("/{post_id}/like", response_model=posts_models.PostSuccessResponse)
async def like_post(
        post_id: int,
        conn: Connection = Depends(get_conn),
        session: Session = Depends(get_session),
        cache: redis.Redis = Depends(get_redis)
):
    if not (post := await posts.get_post(
            conn=conn,
            post_id=post_id
    )):
        return await error_404()

    posts_likes = (await redis.get(
        f"post_{post_id}",
        conn=cache
    )).get("likes", [])
    if session.session_user_id in posts_likes:
        posts_likes.remove(session.session_user_id)
    else:
        posts_likes.append(session.session_user_id)
    await redis.set(
        f"post_{post_id}",
        value={
            'likes': posts_likes
        },
        conn=cache
    )
    post.likes = posts_likes
    return posts_models.PostSuccessResponse(
        data=post
    )


async def add_post_likes_to_model(
        cache: redis.Redis,
        model: posts_models.Post
) -> posts_models.Post:
    model.likes = (
        await redis.get(
            key=f"post_{model.id}",
            conn=cache
        )
    ).get('likes', [])
    return model
