from pydantic import BaseModel
from typing import List

class UserForm(BaseModel):
    login: str
    password: str
    block_state: bool = False




