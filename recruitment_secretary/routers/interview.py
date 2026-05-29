import json
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import Response
from sqlalchemy.orm import Session

from database import get_db
from models import Application, InterviewSession, InterviewResult, ApplicationStatus
from schemas import StartInterviewResponse, InterviewResultOut
from services.phone_interview import (
    INTERVIEW_QUESTIONS,
    initiate_call,
    validate_twilio_signature,
    build_twiml_question,
    build_twiml_goodbye,
    append_transcript,
    format_transcript_for_summary,
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

    call_info = await initiate_call(application_id, phone)

    # Create or update interview session
    session = application.interview_session
    if not session:
        session = InterviewSession(
            application_id=application_id,
            call_sid=call_info.get("call_sid"),
            current_question_index=0,
            transcript="",
        )
        db.add(session)
    else:
        session.call_sid = call_info.get("call_sid")
        session.current_question_index = 0
        session.transcript = ""
        session.is_complete = False

    db.commit()

    return StartInterviewResponse(
        call_sid=call_info.get("call_sid"),
        message="전화 인터뷰가 시작되었습니다." if not call_info.get("is_mock") else "[MOCK] 전화 인터뷰 모의 시작",
        is_mock=call_info.get("is_mock", True),
    )


@router.post("/webhook/voice")
async def voice_webhook(
    request: Request,
    application_id: int,
    db: Session = Depends(get_db),
):
    """
    Twilio calls this on call answer and after each Gather response.
    Query param: application_id
    Form params: CallSid, SpeechResult (from Gather)
    """
    form_data = await request.form()
    params = dict(form_data)

    # Validate Twilio signature
    import os
    base_url = os.getenv("PUBLIC_BASE_URL", "")
    webhook_url = f"{base_url}/interview/webhook/voice?application_id={application_id}"
    signature = request.headers.get("X-Twilio-Signature", "")
    if not validate_twilio_signature(webhook_url, params, signature):
        raise HTTPException(status_code=403, detail="Invalid Twilio signature")

    call_sid = params.get("CallSid", "")
    speech_result = params.get("SpeechResult", "")

    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        return Response(content=build_twiml_goodbye(), media_type="application/xml")

    session = application.interview_session
    if not session:
        session = InterviewSession(
            application_id=application_id,
            call_sid=call_sid,
            current_question_index=0,
            transcript="",
        )
        db.add(session)
        db.flush()

    # Store the answer to the previous question (if any)
    if speech_result and session.current_question_index > 0:
        prev_q = INTERVIEW_QUESTIONS[session.current_question_index - 1]
        session.transcript = append_transcript(session.transcript, prev_q, speech_result)

    # Check if we've exhausted all questions
    if session.current_question_index >= len(INTERVIEW_QUESTIONS):
        session.is_complete = True
        application.status = ApplicationStatus.INTERVIEW_DONE
        db.commit()

        # Generate AI summary asynchronously after hanging up
        transcript_text = format_transcript_for_summary(session.transcript)
        summary_result = await summarize_interview(transcript_text, application.position)

        result = InterviewResult(
            application_id=application_id,
            call_sid=call_sid,
            transcript=session.transcript,
            ai_summary=summary_result.get("ai_summary"),
            score=summary_result.get("score"),
            passed=summary_result.get("passed"),
            is_mock=summary_result.get("is_mock", False),
        )
        db.add(result)
        db.commit()

        return Response(content=build_twiml_goodbye(), media_type="application/xml")

    # Ask the next question
    current_q = INTERVIEW_QUESTIONS[session.current_question_index]
    session.current_question_index += 1
    session.updated_at = datetime.now(timezone.utc)
    db.commit()

    gather_url = f"{os.getenv('PUBLIC_BASE_URL', '')}/interview/webhook/voice?application_id={application_id}"
    twiml = build_twiml_question(current_q, gather_url)
    return Response(content=twiml, media_type="application/xml")


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
