from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from main import schemas, crud
from main.dependencies import get_db
from main.schemas import RestfulModel, UserInfo, User, UserCreate, Token
from main.settings import get_settings
from main.utils.jwt_util import get_current_user, authenticate_user, create_access_token

router = APIRouter(prefix="/api/v1/users", tags=["User"])


@router.get("/getUserList", response_model=RestfulModel[list[schemas.User]])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return RestfulModel.success(users)


@router.get("/getUser/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get('/info', response_model=RestfulModel[UserInfo])
async def user_info(current_user: User = Depends(get_current_user)):
    return RestfulModel.success(UserInfo(username=current_user.username,
                                         email=current_user.email, roles=[r.role_name for r in current_user.roles]))


@router.post("/login", response_model=RestfulModel[Token])
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)):
    setting = get_settings()
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return RestfulModel.success({"access_token": access_token, "token_type": "bearer"})
