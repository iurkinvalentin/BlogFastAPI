from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from data.database import SessionLocal
from schemas.user import User, UserRead, UserCreate, UserInDB
from views import auth


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(auth.get_current_user)):
    return current_user


@router.post('/register/', response_model=UserRead)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return auth.register_handler(user_data, db)


@router.delete('/users/{user_id}')
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(auth.get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нельзя удалить другого пользователя"
        )
    return auth.delete_user_handler(user_id, db)
