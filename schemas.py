#
#  ___________________
#  Import LIBRARIES
from enum import Enum
from pydantic import BaseModel, Field
#  Import FILES
#  ___________________


# Enum class for predefined video categories.
class VideoCategory(str, Enum):
    TECH = "tech"
    GAMING = "gaming"
    MUSIC = "music"


class Video(BaseModel):
    id: int
    title: str = Field(
        ..., min_length=3, max_length=50
    )  # Title with length constraints
    description: str | None = Field(None, max_length=200)
    # Optional description with max length
    category: VideoCategory  # Category using the predefined Enum
    views: int = Field(..., ge=0)  # Views must be a non-negative integer
    likes: int = Field(..., ge=0)  # Likes must be a non-negative integer


# {
#   "id": 5,
#   "title": "Learn SQLModel",
#   "description": "SQLModel from zero to Hero",
#   "category": "tech",
#   "views": 70000,
#   "likes": 600
# }

# {
#   "id": 6,
#   "title": "Demons",
#   "description": "Imagine Dragons",
#   "category": "music",
#   "views": 32381815,
#   "likes": 283848
# }
