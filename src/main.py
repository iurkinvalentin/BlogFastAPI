from fastapi import FastAPI
from routers import blog, user, auth

app = FastAPI(
    title='blog',
    description='Gростое API блог приложение',
    version='0.1'
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(blog.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)
