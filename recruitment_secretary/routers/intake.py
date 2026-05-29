import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Applicant, Application, SourcePlatform, ApplicationStatus
from schemas import (
    WantedWebhookPayload, RememberWebhookPayload,
    GroupbyWebhookPayload, EmailIntakePayload, IntakeResponse,
)
from services.intake_parser import parse_wanted, parse_remember, parse_groupby, parse_email
from auth import require_api_key

router = APIRouter(prefix="/intake", tags=["intake"])


def _upsert_applicant(db: Session, name: str, email: str, phone: str = None) -> Applicant:
    applicant = db.query(Applicant).filter(Applicant.email == email).first()
    if not applicant:
        applicant = Applicant(name=name, email=email, phone=phone)
        db.add(applicant)
        db.flush()
    return applicant


def _create_application(
    db: Session,
    applicant: Applicant,
    normalized: dict,
    platform: SourcePlatform,
    raw: dict,
) -> Application:
    app = Application(
        applicant_id=applicant.id,
        position=normalized["position"],
        source_platform=platform,
        external_id=normalized.get("external_id"),
        resume_url=normalized.get("resume_url"),
        cover_letter=normalized.get("cover_letter"),
        status=ApplicationStatus.RECEIVED,
        raw_payload=json.dumps(raw, ensure_ascii=False),
    )
    db.add(app)
    db.commit()
    db.refresh(app)
    return app


@router.post("/wanted", response_model=IntakeResponse)
async def intake_wanted(
    payload: WantedWebhookPayload,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    normalized = parse_wanted(payload.model_dump())
    applicant = _upsert_applicant(db, normalized["name"], normalized["email"], normalized.get("phone"))
    application = _create_application(db, applicant, normalized, SourcePlatform.WANTED, payload.model_dump())
    return IntakeResponse(
        application_id=application.id,
        applicant_id=applicant.id,
        message=f"원티드 지원서 접수 완료 (application #{application.id})",
    )


@router.post("/remember", response_model=IntakeResponse)
async def intake_remember(
    payload: RememberWebhookPayload,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    normalized = parse_remember(payload.model_dump())
    applicant = _upsert_applicant(db, normalized["name"], normalized["email"], normalized.get("phone"))
    application = _create_application(db, applicant, normalized, SourcePlatform.REMEMBER, payload.model_dump())
    return IntakeResponse(
        application_id=application.id,
        applicant_id=applicant.id,
        message=f"리멤버 지원서 접수 완료 (application #{application.id})",
    )


@router.post("/groupby", response_model=IntakeResponse)
async def intake_groupby(
    payload: GroupbyWebhookPayload,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    normalized = parse_groupby(payload.model_dump())
    applicant = _upsert_applicant(db, normalized["name"], normalized["email"], normalized.get("phone"))
    application = _create_application(db, applicant, normalized, SourcePlatform.GROUPBY, payload.model_dump())
    return IntakeResponse(
        application_id=application.id,
        applicant_id=applicant.id,
        message=f"그룹바이 지원서 접수 완료 (application #{application.id})",
    )


@router.post("/email", response_model=IntakeResponse)
async def intake_email(
    payload: EmailIntakePayload,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    normalized = parse_email(payload.model_dump())
    applicant = _upsert_applicant(db, normalized["name"], normalized["email"], normalized.get("phone"))
    application = _create_application(db, applicant, normalized, SourcePlatform.EMAIL, payload.model_dump())
    return IntakeResponse(
        application_id=application.id,
        applicant_id=applicant.id,
        message=f"이메일 지원서 접수 완료 (application #{application.id})",
    )
