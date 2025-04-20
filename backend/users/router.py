from fastapi import APIRouter, Request, HTTPException
from users.repository import UserRepo
from users.schemas import UserForm


router = APIRouter(
    prefix="/auth",
    tags=["Users"]
)


@router.post("/register")
async def register_user(request: Request, user: UserForm):
    current_user = await UserRepo.find_one_or_none(login=user.login)
    print(current_user)
    if not current_user:
        await UserRepo.add(login=user.login, password=user.password, block_state=user.block_state)
    else:
        raise HTTPException(status_code=403, detail="User already exists")