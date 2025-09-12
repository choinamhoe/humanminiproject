#pip install uvicorn fastapi dotenv
import uvicorn, sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.config import config, cors_config
from routes.golfRouter import router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    **cors_config
)
@app.get("/")
async def test():
    from fastapi.responses import JSONResponse
    from fastapi import status
    return JSONResponse({
        "message":"aaa"
    }, status_code=status.HTTP_200_OK)
app.include_router(router, prefix="")

if __name__ == "__main__":
    print("메인 호출")
    try:
        uvicorn.run(
            "main:app", 
            host="0.0.0.0", port=config["BACKEND_PORT"], reload=True)
    except Exception as e:
        sys.exit(1)
