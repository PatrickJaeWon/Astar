import json
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from database import get_db
from models import Application, InterviewSchedule, ApplicationStatus
from schemas import SendInviteResponse, ConfirmScheduleRequest, ScheduleOut
from services.notification import (
    generate_confirmation_token,
    generate_available_slots,
    send_interview_invite_email,
    send_interview_invite_sms,
)
from auth import require_api_key

router = APIRouter(prefix="/schedule", tags=["schedule"])


@router.post("/send-invite/{application_id}", response_model=SendInviteResponse)
async def send_invite(
    application_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="지원서를 찾을 수 없습니다.")

    review = application.review
    if not review or not review.passed:
        raise HTTPException(
            status_code=400,
            detail="서류 심사를 통과한 지원서만 인터뷰 초대를 발송할 수 있습니다.",
        )

    if application.schedule:
        raise HTTPException(status_code=409, detail="이미 인터뷰 초대가 발송된 지원서입니다.")

    slots = generate_available_slots(3)
    token = generate_confirmation_token()

    schedule = InterviewSchedule(
        application_id=application.id,
        available_slots=json.dumps(slots),
        confirmation_token=token,
        invite_sent_at=datetime.now(timezone.utc),
    )
    db.add(schedule)
    db.flush()

    applicant = application.applicant
    email_sent = await send_interview_invite_email(
        to_email=applicant.email,
        to_name=applicant.name,
        position=application.position,
        available_slots=slots,
        confirmation_token=token,
    )
    sms_sent = False
    if applicant.phone:
        sms_sent = await send_interview_invite_sms(
            to_phone=applicant.phone,
            to_name=applicant.name,
            position=application.position,
            available_slots=slots,
            confirmation_token=token,
        )

    schedule.email_sent = email_sent
    schedule.sms_sent = sms_sent
    application.status = ApplicationStatus.INTERVIEW_INVITED
    db.commit()
    db.refresh(schedule)

    return SendInviteResponse(
        schedule_id=schedule.id,
        email_sent=email_sent,
        sms_sent=sms_sent,
        available_slots=slots,
        confirmation_token=token,
        message="인터뷰 초대 발송 완료" + (" (이메일/SMS 모두 모의 발송)" if not email_sent else ""),
    )


@router.get("/confirm", response_class=HTMLResponse)
async def confirm_schedule_via_link(
    token: str = Query(...),
    slot: str = Query(...),
    db: Session = Depends(get_db),
):
    """Candidate clicks this GET link from email/SMS to confirm a time slot."""
    schedule = db.query(InterviewSchedule).filter(
        InterviewSchedule.confirmation_token == token
    ).first()
    if not schedule:
        return HTMLResponse("<h2>유효하지 않은 확인 링크입니다.</h2>", status_code=404)
    if schedule.is_confirmed:
        confirmed = schedule.confirmed_slot.strftime("%Y년 %m월 %d일 %H:%M") if schedule.confirmed_slot else "확인 중"
        return HTMLResponse(f"<h2>이미 확정된 일정이 있습니다 ({confirmed}).</h2>", status_code=200)

    # Restore the '+' that HTTP query-string decoding turns into a space
    slot_normalized = slot.replace(" ", "+")
    available = json.loads(schedule.available_slots or "[]")
    if slot_normalized not in available:
        return HTMLResponse("<h2>선택한 시간이 제안된 일정에 없습니다.</h2>", status_code=400)

    schedule.confirmed_slot = datetime.fromisoformat(slot_normalized)
    schedule.is_confirmed = True
    schedule.application.status = ApplicationStatus.INTERVIEW_SCHEDULED
    db.commit()

    from services.notification import _fmt_slot
    formatted = _fmt_slot(slot)
    return HTMLResponse(
        f"<h2>인터뷰 일정이 확정되었습니다!</h2><p>선택하신 일정: <strong>{formatted}</strong></p>"
        f"<p>인터뷰 당일 연락드리겠습니다. 감사합니다.</p>",
        status_code=200,
    )


@router.post("/confirm")
async def confirm_schedule(
    request: ConfirmScheduleRequest,
    db: Session = Depends(get_db),
):
    """JSON API version for programmatic confirmation — no API key required."""
    schedule = db.query(InterviewSchedule).filter(
        InterviewSchedule.confirmation_token == request.confirmation_token
    ).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="유효하지 않은 확인 토큰입니다.")
    if schedule.is_confirmed:
        raise HTTPException(status_code=409, detail="이미 확정된 일정이 있습니다.")

    available = json.loads(schedule.available_slots or "[]")
    if request.selected_slot not in available:
        raise HTTPException(status_code=400, detail="선택한 시간이 제안된 일정에 없습니다.")

    schedule.confirmed_slot = datetime.fromisoformat(request.selected_slot)
    schedule.is_confirmed = True
    schedule.application.status = ApplicationStatus.INTERVIEW_SCHEDULED
    db.commit()

    return {
        "message": "인터뷰 일정이 확정되었습니다.",
        "confirmed_slot": request.selected_slot,
        "application_id": schedule.application_id,
    }


@router.get("/{application_id}", response_model=ScheduleOut)
async def get_schedule(
    application_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    schedule = db.query(InterviewSchedule).filter(
        InterviewSchedule.application_id == application_id
    ).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="인터뷰 일정 정보가 없습니다.")
    return schedule
