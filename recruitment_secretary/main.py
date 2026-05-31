from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from database import Base, engine
import models  # ensure all models are registered before create_all

from routers import intake, review, schedule, interview, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="채용 비서 (Recruitment Secretary)",
    description=(
        "원티드 / 리멤버 / 그룹바이 지원서 통합 수집 → AI 서류 심사 → "
        "인터뷰 일정 조율 (이메일/SMS) → AI 전화 인터뷰"
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(intake.router)
app.include_router(review.router)
app.include_router(schedule.router)
app.include_router(interview.router)
app.include_router(dashboard.router)

_static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=_static_dir), name="static")


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/ui")


@app.get("/ui", include_in_schema=False)
async def ui():
    return FileResponse(os.path.join(_static_dir, "index.html"))
