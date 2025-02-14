from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models.blog import Blog, Like, Rating


def create_blog_handler(blog_data, db: Session):
    db_blog = Blog(**blog_data.dict())
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog


def read_blogs_handler(skip: int, limit: int, db: Session):
    try:
        blogs = db.query(Blog).offset(skip).limit(limit).all()
        return blogs
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail='Ошибка чтения базы данных') from e


def read_one_handler(blog_id, db: Session):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail='Блог не найден')
    return blog


def update_blog_handler(blog_id: int, blog_data, db: Session):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail='Блог не найден')

    if isinstance(blog_data, dict):
        updated_data = blog_data
    else:
        updated_data = blog_data.dict(exclude_unset=True)

    for key, value in updated_data.items():
        setattr(blog, key, value)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Конфликт данных при обновлении блога"
        ) from e
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Ошибка обновления данных в базе"
        ) from e

    db.refresh(blog)
    return blog


def delete_blog_handler(blog_id, db: Session):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail='Блог не найден')
    db.delete(blog)
    db.commit()
    return {'detail': 'Блог успешно удален'}


def like_handler(like_data, db: Session, current_user):
    blog = db.query(Blog).filter(Blog.id == like_data.blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Пост не найден")
    existing_like = db.query(Like).filter(
        Like.user_id == current_user.id,
        Like.blog_id == like_data.blog_id).first()
    if existing_like:
        db.delete(existing_like)
        db.commit()
        return {"message": "Лайк удалён"}
    new_like = Like(user_id=current_user.id, blog_id=like_data.blog_id)
    db.add(new_like)
    db.commit()
    return {"message": "Лайк добавлен"}


def rating_handler(rating_data, db: Session, current_user):
    blog = db.query(Blog).filter(Blog.id == rating_data.blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Пост не найден")
    existing_rating = db.query(
        Rating).filter(
            Rating.user_id == current_user.id,
            Rating.blog_id == rating_data.blog_id).first()
    if existing_rating:
        existing_rating.rating = rating_data.rating
    else:
        new_rating = Rating(
            user_id=current_user.id, blog_id=rating_data.blog_id,
            rating=rating_data.rating)
        db.add(new_rating)

    db.commit()
    return {"message": "Рейтинг обновлён"}
