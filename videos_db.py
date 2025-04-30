#
#  ___________________
#  Import LIBRARIES
#  Import FILES
from schemas import Video, VideoCategory
#  ___________________


videos = {
    1: Video(
        id=1,
        title="FastAPI Tutorial",
        description="Learn FastAPI basics",
        category=VideoCategory.TECH,
        views=1500,
        likes=200,
    ),
    2: Video(
        id=2,
        title="Python for Beginners",
        description="Introduction to Python",
        category=VideoCategory.TECH,
        views=1200,
        likes=150,
    ),
    3: Video(
        id=3,
        title="Gaming Setup Tour",
        description="My gaming setup",
        category=VideoCategory.GAMING,
        views=800,
        likes=100,
    ),
    4: Video(
        id=4,
        title="Guitar Lesson 1",
        description="Beginner guitar lesson",
        category=VideoCategory.MUSIC,
        views=2000,
        likes=300,
    ),
}
