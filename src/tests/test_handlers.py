import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException

from models.blog import Blog, Base
from views.blog import (
    create_blog_handler,
    read_one_handler,
    update_blog_handler,
    delete_blog_handler
)
from schemas.blog import BlogCreate, BlogUpdate


@pytest.fixture(scope="module")
def test_db():
    engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()


def test_create_blog_handler(test_db):
    blog_data = BlogCreate(
        title="Test Blog", text="This is a test blog", is_published=True)
    created_blog = create_blog_handler(blog_data, test_db)
    assert created_blog.id is not None
    assert created_blog.title == "Test Blog"
    assert created_blog.text == "This is a test blog"


def test_read_one_handler(test_db):
    blog_data = BlogCreate(
        title="Read Blog", text="Read test", is_published=True)
    created_blog = create_blog_handler(blog_data, test_db)
    blog = read_one_handler(created_blog.id, test_db)
    assert blog.id == created_blog.id
    assert blog.title == "Read Blog"


def test_update_blog_handler(test_db):
    blog_data = BlogCreate(
        title="Update Blog", text="Initial text", is_published=True)
    created_blog = create_blog_handler(blog_data, test_db)
    update_data = BlogUpdate(text="Updated text")
    updated_blog = update_blog_handler(created_blog.id, update_data, test_db)
    assert updated_blog.text == "Updated text"
    assert updated_blog.title == "Update Blog"


def test_delete_blog_handler(test_db):
    blog_data = BlogCreate(
        title="Delete Blog", text="Delete test", is_published=True)
    created_blog = create_blog_handler(blog_data, test_db)
    response = delete_blog_handler(created_blog.id, test_db)
    assert response["detail"] == "Блог успешно удален"
    with pytest.raises(HTTPException):
        read_one_handler(created_blog.id, test_db)
