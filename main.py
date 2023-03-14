from fastapi import FastAPI, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import files, users

app = FastAPI()

origins = [
    # "http://127.0.0.1:5173",
    "*"
]

app.include_router(users.router)
app.include_router(files.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


