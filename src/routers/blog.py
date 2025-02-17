from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from data.database import get_db
from views.blog import (
    create_blog_handler, read_blogs_handler,
    update_blog_handler, delete_blog_handler,
    read_one_handler, like_handler,
    rating_handler, get_comments_handler, add_comment_handler,
    delete_comment_handler)
from schemas.blog import (
    BlogCreate, BlogResponse, BlogUpdate,
    LikeCreate, RatingCreate, CommentCreate, CommentResponse)
from typing import List
from views import auth


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


@router.post('/')
def like_blog(like_data: LikeCreate, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    return like_handler(like_data, db, current_user)


@router.post('/')
def rating_blog(rating_data: RatingCreate, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    return rating_handler(rating_data, db, current_user)


@router.post('/')
def add_comment(comment_data: CommentCreate, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    return add_comment_handler(comment_data, db, current_user)


@router.get("/{blog_id}", response_model=List[CommentResponse])
def get_comments(blog_id: int, db: Session = Depends(get_db)):
    return get_comments_handler(blog_id, db)


@router.delete("/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    return delete_comment_handler(comment_id, db, current_user)
