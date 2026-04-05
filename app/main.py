from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .db import engine, Base
from .api import router

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospitality Event Search API")

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://utopia-hackathon.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
