import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import posts, users, auth
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)



app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware, # Middlewares run before every request
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router) #Includes post router to the app
app.include_router(users.router) 
app.include_router(auth.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,port=8002, host="0.0.0.0")
