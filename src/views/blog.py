from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models.blog import Blog


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


def update_blog_handler(blog_id, blog_data, db: Session):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail='Блог не найден')
    updated_data = blog_data.dict(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(blog, key, value)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Конфликт данных при обновлении блога") from e
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Ошибка обновления данных в базе") from e
    db.refresh(blog)
    return blog


def delete_blog_handler(blog_id, db: Session):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail='Блог не найден')
    db.delete(blog)
    db.commit()
    return {'detail': 'Блог успешно удален'}
