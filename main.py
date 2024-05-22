from imp import reload
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from ab_app.routers import router as api_router
from ab_app.models import build_models

app = FastAPI()

build_models()

origins = ["http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, log_level="info", reload=True)
    print("running")