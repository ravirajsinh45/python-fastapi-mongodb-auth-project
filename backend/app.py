import os, sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from modules.config import settings
from modules.auth import auth, user


#If code is running in production environment turn off the documentation
if settings.ENV=="prod":
    app = FastAPI(docs_url=None, redoc_url=None)
else:
    app = FastAPI()


origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Adding route defined in internal files
app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')
app.include_router(user.router, tags=['Users'], prefix='/api/users')


#To check weather app is running or not
@app.get("/api/health")
def root():
    return {"message": "Welcome to FastAPI with MongoDB"}





if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True)
