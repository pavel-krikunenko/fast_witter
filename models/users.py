from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class BaseUser(BaseModel):
    id: int = 0
    en: Optional[bool]
    name: str = ''
    join_date: Optional[datetime] = None

    @property
    def is_authenticated(self):
        return bool(self.id)


class Anonymous(BaseUser):
    ...


class User(BaseUser):
    ...

