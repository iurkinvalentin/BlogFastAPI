from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from data.database import get_db
from views.blog import (
    create_blog_handler, read_blogs_handler,
    update_blog_handler, delete_blog_handler,
    read_one_handler)
from schemas.blog import (
    BlogCreate, BlogResponse, BlogUpdate)
from typing import List


router = APIRouter()


@router.post('/', response_model=BlogResponse)
def create_blog(blog: BlogCreate, db: Session = Depends(get_db)):
    return create_blog_handler(blog, db)


@router.get('/', response_model=List[BlogResponse])
def read_blogs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return read_blogs_handler(skip, limit, db)


@router.get('/{blog_id}', response_model=BlogResponse)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    return read_one_handler(blog_id, db)


@router.patch('/{blog_id}', response_model=BlogResponse)
def update_blog(blog_id: int, blog_update: BlogUpdate, db: Session = Depends(get_db)):
    return update_blog_handler(blog_id, blog_update, db)


@router.delete('/{blog_id}')
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    return delete_blog_handler(blog_id, db)
