from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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


@app.get("/", tags=["health"])
async def health_check():
    return {
        "status": "ok",
        "service": "recruitment-secretary",
        "version": "1.0.0",
        "endpoints": [
            "POST /intake/wanted",
            "POST /intake/remember",
            "POST /intake/groupby",
            "POST /intake/email",
            "POST /review/{application_id}",
            "GET  /review/{application_id}",
            "POST /schedule/send-invite/{application_id}",
            "POST /schedule/confirm",
            "GET  /schedule/{application_id}",
            "POST /interview/start/{application_id}",
            "POST /interview/webhook/vapi",
            "GET  /interview/{application_id}/result",
            "GET  /dashboard/applications",
            "GET  /dashboard/stats",
        ],
    }
