
from passlib.hash import bcrypt


async def get_password_hash(password: str, salt: str) -> str:
    return bcrypt.using(salt=salt).hash(password)
