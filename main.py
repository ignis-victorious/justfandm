#
#  ___________________
#  Import LIBRARIES
from fastapi import FastAPI, HTTPException, Depends, status
from typing import Any
from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi.responses import HTMLResponse
from models import UserCreate, UserBase, User, PostCreate, Post, CommentCreate, Comment

#  Import FILES
from db_db import db
#  ___________________


# main.py
app = FastAPI(title="Blog API")


# root endpoint
@app.get("/", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    """
    Root endpoint that serves the index.html file as an HTML response.

    :return: Contents of index.html
    """
    with open("index.html", "r") as f:
        # Read and return the contents of index.html as an HTML response
        return HTMLResponse(
            content=f.read(), status_code=200
        )  # Accessible at http://0.0.0.0:8000/


# Dependency to get current user (simplified auth)
async def get_current_user(user_id: UUID) -> UserBase:
    user = db["users"].get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


################ Users Endpoints ################
@app.post("/users/", response_model=UserBase, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate) -> dict[str, Any]:
    user_id: UUID = uuid4()
    current_time: datetime = datetime.now(timezone.utc)

    new_user: dict[str, Any] = {
        "id": user_id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "bio": user.bio,
        "created_at": current_time,
        "updated_at": None,
        "is_active": True,
        "posts": [],
        "comments": [],
    }

    db["users"][user_id] = new_user
    return new_user


@app.get("/users/", response_model=list[UserBase])
async def get_users() -> list[UserBase]:
    return list(db["users"].values())


@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: UUID) -> User:
    if user_id not in db["users"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not  found"
        )
    return db["users"][user_id]


################ Posts Endpoints ################
@app.post("/users/{user_id}/posts/", response_model=Post)
async def create_post(
    user_id: UUID, post: PostCreate, current_user: UserBase = Depends(get_current_user)
) -> dict[str, Any]:
    post_id: UUID = uuid4()
    current_time: datetime = datetime.now(timezone.utc)

    new_post: dict[str, Any] = {
        "id": post_id,
        "title": post.title,
        "content": post.content,
        "created_at": current_time,
        "updated_at": None,
        "published": post.published,
        "author_id": user_id,
        "author": db["users"][user_id],
        "comments": [],
    }

    db["posts"][post_id] = new_post
    db["users"][user_id]["posts"].append(new_post)
    return new_post


@app.get("/posts/", response_model=list[Post])
async def get_posts() -> list[Post]:
    return list(db["posts"].values())


@app.get("/posts/{post_id}", response_model=Post)
async def get_post(post_id: UUID) -> Post:
    if post_id not in db["posts"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return db["posts"][post_id]


################ Comments Endpoints ################
@app.post("/posts/{post_id}/comments/", response_model=Comment)
async def create_comment(
    post_id: UUID,
    comment: CommentCreate,
    current_user: UserBase = Depends(get_current_user),
) -> dict[str, Any]:
    if post_id not in db["posts"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    comment_id: UUID = uuid4()
    current_time: datetime = datetime.now(timezone.utc)

    new_comment = {
        "id": comment_id,
        "content": comment.content,
        "created_at": current_time,
        "updated_at": None,
        "author_id": current_user["id"],
        "post_id": post_id,
        "author": current_user,
    }

    db["comments"][comment_id] = new_comment
    db["posts"][post_id]["comments"].append(new_comment)
    db["users"][current_user["id"]]["comments"].append(new_comment)
    return new_comment


@app.get("/posts/{post_id}/comments/", response_model=list[Comment])
async def get_post_comments(post_id: UUID) -> list[Comment]:
    if post_id not in db["posts"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return db["posts"][post_id]["comments"]


# Application Entry Point
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )


#
#  ___________________
#  Import LIBRARIES
#  Import FILES
#  ___________________


# def main():
#     print("Hello from justfandm!")
