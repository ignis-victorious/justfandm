#
#  ___________________
#  Import LIBRARIES
from typing import Any
from fastapi import FastAPI, Path, Query, HTTPException
from starlette.responses import HTMLResponse
import os


#  Import FILES
from schemas import Video, VideoCategory
from videos_db import videos
#  ___________________


# =================================================================
# Section 1: Initializing the FastAPI App
# =================================================================

app = FastAPI(
    title="FastAPI Path, Query, and Predefined Parameters",  # Title of the API
    description="FastApi and SQLModel Modern Tutorial",  # Description for the API documentation
    version="1.0.0",  # Version of the API
)

# api_router = APIRouter()
# app.include_router(api_router)


# =================================================================
# Section 2: Defining Enums and Data Models
# =================================================================
#  See schemas.py

# =================================================================
# Section 3: Creating an In-Memory Database
# =================================================================
#  See videos_db.py

# =================================================================
# Section 4: Removed old Root and oreplaced with html_page Endpoint
# =================================================================


# Load HTML file from root
@app.get("/", response_class=HTMLResponse)
async def html_page() -> HTMLResponse:
    """
    Root endpoint that serves the index.html file as an HTML response.

    :return: Contents of index.html
    """
    # display index.html
    with open("index.html", "r") as f:
        # Read and return the contents of index.html as an HTML response
        return HTMLResponse(
            content=f.read(), status_code=200
        )  # Accessible at htto://0.0.0.0:8000/


# =========================================
# Section 5: Fetching All Videos
# =========================================
@app.get("/videos/", response_model=list[Video])
async def get_videos() -> list[Video]:
    """
    Retrieve a list of videos with a default limit of 10.

    :return: A list of up to 10 video objects.

    Accessible at http://0.0.0.0:8000/videos/
    """
    return list(videos.values())[:10]  # Return the first 10 videos


# =========================================
# Section 6: Retrieving a Single Video by ID
# =========================================
@app.get("/videos/{video_id}")
async def get_video(
    video_id: int = Path(..., gt=0, description="ID of the video"),
) -> Video:
    """
    Retrieve a video by its ID.

    :param video_id: The ID of the video to retrieve.
    :return: The video object if found.
    :raises HTTPException: If the video with the given ID is not found.
    """
    if video_id not in videos:
        # Raise a 404 error if the video ID does not exist
        raise HTTPException(status_code=404, detail="Video not found")
    return videos[video_id]  # Accessible at http://0.0.0.0:8000/videos/1


# =========================================
# Section 7: Filtering Videos by Category with Pagination
# =========================================
@app.get("/categories/{category}/videos")
async def get_videos_by_category(
    category: VideoCategory,  # Path parameter using the VideoCategory Enum
    limit: int = Query(
        10, gt=0, le=100, description="Maximum number of videos to return"
    ),  # Query parameter for limit with default 10 and max 100
    skip: int = Query(
        0, ge=0, description="Number of videos to skip"
    ),  # Query parameter for skip with default 0
) -> list[Video]:
    """
    Retrieve videos filtered by category with pagination.

    :param category: The category of videos to filter by (tech, gaming, music).
    :param limit: Maximum number of videos to return (default is 10, max 100).
    :param skip: Number of videos to skip for pagination (default is 0).
    :return: A list of videos matching the category and pagination parameters.
    """

    # Filter videos based on the specified category
    filtered_videos: list[Video] = [
        video for video in videos.values() if video.category == category
    ]
    # Apply pagination using skip and limit
    # Accessible at http://0.0.0.0:8000/categories/tech/videos?limit=5&skip=1
    return filtered_videos[skip : skip + limit]


# =========================================
# Section 8: Retrieving Video Statistics for a User
# =========================================
@app.get("/users/{user_id}/videos/{video_id}/stats")
async def get_video_stats(
    user_id: int = Path(
        ..., gt=0, description="ID of the user"
    ),  # Path parameter for user ID
    video_id: int = Path(
        ..., gt=0, description="ID of the video"
    ),  # Path parameter for video ID
    watched: bool = Query(
        False, description="Whether the video was watched"
    ),  # Query parameter for watched status
) -> dict[str, Any]:
    """
    Retrieve statistics for a specific video and user.

    :param user_id: The ID of the user requesting the stats.
    :param video_id: The ID of the video for which to retrieve stats.
    :param watched: Indicates if the user has watched the video (default is False).
    :return: A dictionary containing user ID, video ID, watched status, and video data.
    :raises HTTPException: If the video with the given ID is not found.
    """
    if video_id not in videos:
        # Raise a 404 error if the video ID does not exist
        raise HTTPException(status_code=404, detail="Video not found")
    # Accessible at http://0.0.0.0:8000/users/1/videos/1/stats
    return {
        "user_id": user_id,
        "video_id": video_id,
        "watched": watched,
        "video_data": videos[video_id],
    }


# =========================================
# Section 9: Creating a New Video Entry
# =========================================
@app.post("/videos/add", response_model=Video)
async def create_video(video: Video) -> Video:
    """
    Create a new video entry in the database.

    :param video: The video data to be added.
    :return: The video object that was added.
    """
    # Generate a new ID for the video
    new_id: int = max(videos.keys()) + 1
    video.id = new_id
    # Add the video to the database
    videos[new_id] = video
    return video


# =========================================
# Section 10: File Path as parameter
# =========================================
@app.get("/files/{file_path:path}")
async def read_file(file_path: str) -> dict[str, str]:
    """
    Read a file from the specified path.

    :param file_path: The path to the file to read.
    :return: The contents of the file.
    """
    if not os.path.exists(file_path):
        # Raise a 404 error if the file does not exist
        raise HTTPException(status_code=404, detail="File not found")
    with open(file_path, "r") as file:
        return {"file_content": file.read()}


# if __name__ == "__main__":
#     # Use this for debugging purposes only
#     import uvicorn

# uvicorn.run(
#        "pain: app",  # Module and app name
#        host="0.0.0.0",# Host address
#        port=8000, # Port number
#        log_level="debug", # Logging Level
#        reload=True, # Enable auto-reload on code changes
# )


#
#  ___________________
#  Import LIBRARIES
#  Import FILES
#  ___________________


# def main():
#     print("Hello from justfandm!")
