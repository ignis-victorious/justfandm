# 
#  ___________________
#  Import LIBRARIES
from fastapi import FastAPI, APIRouter 
from starlette.responses import HTMLResponse
#  Import FILES
#  ___________________



app = FastAPI(title="Hello World", description="=FastApi and SQLModel Tutorial")

api_router = APIRouter()


# Basic root message
@api_router.get("/", status_code=200)
def root():
    '''
    Root GET
    
    '''
    return {"msg": "Hello, World!"}



# Load HTML file from root
# Capi_router.get("/", response_class=HTMLResponse)
# async def root():
#   display index.html
# with open("index.html", ",") as f:
#     return HTMLResponse(content=f.read(), status_code=200)



app.include_router(api_router)

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn
   
    uvicorn.run( 'main: app', host="o.0.0.0", port=8001,log_level="debug", reload=True)
    



# 
#  ___________________
#  Import LIBRARIES
#  Import FILES
#  ___________________
# def main():
#     print("Hello from justfandm!")



