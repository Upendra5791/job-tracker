from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, jobs
from app.database import create_db_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    create_db_tables()
    yield
    print("Shutting down...")


app = FastAPI(title="Job Tracker API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # update to allow frontend localhost only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Job Tracker API!"}


app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])
# app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
# app.include_router(stats.router, prefix="/api/stats", tags=["stats"])
