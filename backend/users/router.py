from fastapi import APIRouter, Request, HTTPException
from users.repository import UserRepo
from users.schemas import UserForm, UserLoginForm


router = APIRouter(
    prefix="/auth",
    tags=["Users"]
)


@router.post("/register")
async def register_user(request: Request, user: UserForm):
    current_user = await UserRepo.find_one_or_none(login=user.login)
    if not current_user:
        await UserRepo.add(login=user.login, password=user.password, block_state=user.block_state)
    else:
        raise HTTPException(status_code=403, detail="User already exists")


@router.post("/login")
async def register_user(request: Request, user: UserLoginForm):
    current_user = await UserRepo.find_one_or_none(login=user.username)
    if current_user:
        raise HTTPException(status_code=200, detail="Login succesfully")
    else:
        raise HTTPException(status_code=403, detail="User already exists")
