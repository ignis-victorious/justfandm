#
#  ___________________
#  Import LIBRARIES
from pydantic import BaseModel, field_validator, EmailStr, Field, ConfigDict, SecretStr
from datetime import datetime, timezone
from uuid import UUID, uuid4
from pprint import pp, pprint
#  Import FILESatetime import datetime, timezone
#  ___________________
# models.py


############## Base models (for responses) ##############
class UserBase(BaseModel):
    # Setting from_attributes=True allows the model to populate fields from object attributes, which is useful when
    # dealing with ORM models or other objects where data is accessed via attributes rather than dictionary keys.
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    username: str
    email: EmailStr
    full_name: str
    bio: str | None = None
    created_at: datetime
    updated_at: datetime | None
    is_active: bool


#  ______________ EXAMPLE
print("  UserBase  _________________________")
user_base = UserBase(
    id=uuid4(),
    username="johndoe",
    email="john@example.com",
    full_name="John Doe",
    bio="Python developer",
    created_at=datetime.now(timezone.utc),
    # created_at=datetime.utcnow(),
    updated_at=None,
    is_active=True,
)

pprint(user_base.model_dump())
#  ______________


class PostBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime | None
    published: bool
    author_id: UUID


#  ______________ EXAMPLE
print("  PostBase  _________________________")
post_base = PostBase(
    id=uuid4(),
    title="Getting Started with FastAPI",
    content="FastAPI is a modern web framework...",
    created_at=datetime.now(timezone.utc),
    updated_at=None,
    published=True,
    author_id=user_base.id,
)

pprint(post_base.model_dump())
#  ______________


class CommentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    content: str
    created_at: datetime
    updated_at: datetime | None
    author_id: UUID
    post_id: UUID


#  ______________ EXAMPLE
print("  CommentBase  _________________________")
comment_base = CommentBase(
    id=uuid4(),
    content="Great article! Very helpful.",
    created_at=datetime.now(timezone.utc),
    updated_at=None,
    author_id=user_base.id,
    post_id=post_base.id,
)

pprint(comment_base.model_dump())
#  ______________


############## Request Models (for input validation) ######
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)
    bio: str | None = Field(None, max_length=500)
    password: SecretStr


#  ______________ EXAMPLE
print("  UserCreate  _________________________")
user_create = UserCreate(
    username="johndoe",
    email="john@example.com",
    full_name="John Doe",
    bio="Python developer",
    password="secure123",
)
pprint(user_create.model_dump)
#  ______________


class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    published: bool = False


#  ______________ EXAMPLE
print("  PostCreate  _________________________")
post_create = PostCreate(
    title="Getting Started with FastAPI",
    content="FastAPI is a modern web framework...",
    published=True,
)
pprint(post_create.model_dump())
#  ______________


class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)


#  ______________ EXAMPLE

#  ______________


############ Response models with relationships ############
class Comment(CommentBase):
    author: UserBase


#  ______________ EXAMPLE

print("  Comment _________________________")
pprint(comment_base.model_dump())

print("_________________________")
comment = Comment(**comment_base.model_dump(), author=user_base)
pprint(comment.model_dump())
#  ______________


class Post(PostBase):
    author: UserBase
    comments: list[Comment] = []


#  ______________ EXAMPLE
print("  Post _________________________")
pprint(post_base.model_dump())
print("_________________________")
post = Post(**post_base.model_dump(), author=user_base, comments=[comment])
pprint(post.model_dump())
print("_________________________")
pprint(post.author.bio)
#  ______________


class User(UserBase):
    posts: list[Post] = []
    comments: list[Comment] = []


#  ______________ EXAMPLE
print("  User _________________________")
user = User(**user_base.model_dump(), posts=[post], comments=[comment])
pprint(user.model_dump())
print("_________________________")
user = User(**user_base.model_dump(), posts=[post, post], comments=[comment, comment])
pprint(user.model_dump())
print("_________________________")
print(user.posts)
print("_________________________")
print(user.comments)
#  ______________


# Final example showing how all models work together
# Create a new user
# Create a new user
print("  + new_user _________________________")
new_user = UserCreate(
    username="testuser",
    email="test@example.com",
    full_name="Test User",
    bio="Testing the models",
    password="testpass123",
)

pprint(new_user.model_dump())

print("  + user_response _________________________")
# Simulate user creation response
user_response = UserBase(
    id=uuid4(),
    username=new_user.username,
    email=new_user.email,
    full_name=new_user.full_name,
    bio=new_user.bio,
    created_at=datetime.now(timezone.utc),
    # created_at=datetime.utcnow(),
    updated_at=None,
    is_active=True,
)
pprint(user_response.model_dump())


print("  + full_user _________________________")

# Create a full user response with relationships
full_user = User(**user_response.model_dump(), posts=[post], comments=[comment])
pprint(full_user.model_dump_json(indent=2))
