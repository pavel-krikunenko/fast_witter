import logging

from asyncpg import Connection
from fastapi import APIRouter, Depends

from db import users
from misc.depends.conf import get as get_conf
from misc.depends.db import get as get_db
from misc.depends.session import get as get_session
from misc.handlers import error_401, error_404, error_500, error_400
from misc.password import get_password_hash
from misc.session import Session
from models.auth import MeSuccessResponse, MeResponse, SignIn, SignUp

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.get("/me", response_model=MeSuccessResponse)
async def get_me(
        session: Session = Depends(get_session)
):
    """
    /me returning current user with session key
    """
    return MeSuccessResponse(data=MeResponse(me=session.user, token=session.key))


@router.post('/sign-in', response_model=MeSuccessResponse)
async def login(
        auth_model: SignIn,
        conn: Connection = Depends(get_db),
        config: dict = Depends(get_conf),
        session: Session = Depends(get_session)
):
    if session.user.is_authenticated:
        return await error_401()

    hashed_password = await get_password_hash(auth_model.password, config['salt'])
    user = await users.get_user_by_creds(conn, auth_model.name, hashed_password)
    if not user:
        return error_404()
    session.set_user(user)
    return MeSuccessResponse(data=MeResponse(me=session.user, token=session.key))


@router.post("/sign-up", response_model=MeSuccessResponse)
async def register(
        reg_model: SignUp,
        conn: Connection = Depends(get_db),
        config: dict = Depends(get_conf),
        session: Session = Depends(get_session)
):
    if session.user.is_authenticated:
        return await error_401()

    if await users.get_user_by_name(
            conn=conn,
            name=reg_model.name
    ):
        return await error_400("This name already exist")

    hashed_password = await get_password_hash(reg_model.password, config['salt'])
    new_user = await users.create_user(
        conn=conn,
        name=reg_model.name,
        password=hashed_password
    )
    if not new_user:
        return await error_500()
    session.set_user(new_user)
    return MeSuccessResponse(
        data=MeResponse(
            me=session.user,
            token=session.key
        )
    )


@router.post('/logout', response_model=MeSuccessResponse)
async def logout(
        session: Session = Depends(get_session)
):
    session.reset_user()
    return MeSuccessResponse(data=MeResponse(me=session.user, token=session.key))
