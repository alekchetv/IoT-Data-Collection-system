from database import async_session
from models import User
from sqlalchemy import select
from BaseRepository import BaseREPO
from models import User


class UserRepo(BaseREPO):
    model=User