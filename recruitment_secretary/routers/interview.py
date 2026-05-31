from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from database import get_db
from models import Application, InterviewResult, ApplicationStatus
from schemas import StartInterviewResponse, InterviewResultOut
from services.phone_interview import (
    initiate_call,
    validate_webhook_secret,
    parse_end_of_call_report,
)
from services.ai_reviewer import summarize_interview
from auth import require_api_key

router = APIRouter(prefix="/interview", tags=["interview"])


@router.post("/start/{application_id}", response_model=StartInterviewResponse)
async def start_interview(
    application_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="지원서를 찾을 수 없습니다.")

    if not application.schedule or not application.schedule.is_confirmed:
        raise HTTPException(status_code=400, detail="인터뷰 일정이 확정된 지원서만 전화 인터뷰를 시작할 수 있습니다.")

    if application.interview_result:
        raise HTTPException(status_code=409, detail="이미 인터뷰가 완료된 지원서입니다.")

    phone = application.applicant.phone
    if not phone:
        raise HTTPException(status_code=400, detail="지원자의 전화번호가 등록되어 있지 않습니다.")

    call_info = await initiate_call(application_id, phone, application.position)
    db.commit()

    return StartInterviewResponse(
        call_sid=call_info.get("call_id"),
        message="VAPI 전화 인터뷰가 시작되었습니다." if not call_info.get("is_mock") else "[MOCK] VAPI 전화 인터뷰 모의 시작",
        is_mock=call_info.get("is_mock", True),
    )


@router.post("/webhook/vapi")
async def vapi_webhook(request: Request, db: Session = Depends(get_db)):
    """
    VAPI calls this when a call ends (end-of-call-report).
    Saves the transcript and generates an AI summary.
    """
    secret = request.headers.get("x-vapi-secret")
    if not validate_webhook_secret(secret):
        raise HTTPException(status_code=403, detail="Invalid VAPI webhook secret")

    payload = await request.json()
    report = parse_end_of_call_report(payload)

    # Acknowledge non-report events (status-update, etc.) without processing
    if report is None:
        return {"status": "ignored"}

    application_id = report.get("application_id")
    if not application_id:
        return {"status": "no application_id in metadata"}

    application = db.query(Application).filter(Application.id == int(application_id)).first()
    if not application:
        return {"status": "application not found"}

    if application.interview_result:
        return {"status": "already processed"}

    # AI summary using Claude
    summary_result = await summarize_interview(report["transcript"], application.position)

    result = InterviewResult(
        application_id=application.id,
        call_sid=report["call_id"],
        transcript=report["transcript"],
        ai_summary=summary_result.get("ai_summary"),
        score=summary_result.get("score"),
        passed=summary_result.get("passed"),
        is_mock=summary_result.get("is_mock", False),
    )
    db.add(result)
    application.status = ApplicationStatus.INTERVIEW_DONE
    db.commit()

    return {"status": "ok", "application_id": application.id}


@router.get("/{application_id}/result", response_model=InterviewResultOut)
async def get_interview_result(
    application_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    result = db.query(InterviewResult).filter(InterviewResult.application_id == application_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="인터뷰 결과가 없습니다.")
    return result
