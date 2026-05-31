from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime
from models import ApplicationStatus, SourcePlatform


# ── Applicant ────────────────────────────────────────────────────────────────

class ApplicantBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None


class ApplicantOut(ApplicantBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Application ───────────────────────────────────────────────────────────────

class ApplicationOut(BaseModel):
    id: int
    applicant_id: int
    position: str
    source_platform: SourcePlatform
    external_id: Optional[str]
    resume_url: Optional[str]
    status: ApplicationStatus
    created_at: datetime
    updated_at: datetime
    applicant: ApplicantOut

    model_config = {"from_attributes": True}


# ── Intake payloads (one per platform) ───────────────────────────────────────

class WantedWebhookPayload(BaseModel):
    """Wanted API webhook format."""
    application_id: str
    applicant_name: str
    applicant_email: str
    applicant_phone: Optional[str] = None
    job_title: str
    resume_url: Optional[str] = None
    cover_letter: Optional[str] = None


class RememberWebhookPayload(BaseModel):
    """Remember (리멤버) webhook format."""
    id: str
    name: str
    email: str
    mobile: Optional[str] = None
    position: str
    profile_url: Optional[str] = None
    introduction: Optional[str] = None


class GroupbyWebhookPayload(BaseModel):
    """그룹바이 webhook format."""
    apply_no: str
    user_name: str
    user_email: str
    user_phone: Optional[str] = None
    job_name: str
    resume_link: Optional[str] = None
    self_introduction: Optional[str] = None


class EmailIntakePayload(BaseModel):
    """Manual email-based intake."""
    sender_name: str
    sender_email: str
    sender_phone: Optional[str] = None
    position: str
    resume_text: Optional[str] = None
    cover_letter: Optional[str] = None


class IntakeResponse(BaseModel):
    application_id: int
    applicant_id: int
    message: str


# ── Review ────────────────────────────────────────────────────────────────────

class ReviewResultOut(BaseModel):
    id: int
    application_id: int
    score: Optional[float]
    passed: Optional[bool]
    summary: Optional[str]
    strengths: Optional[str]
    weaknesses: Optional[str]
    recommendation: Optional[str]
    reviewed_at: datetime
    is_mock: bool

    model_config = {"from_attributes": True}


# ── Schedule ──────────────────────────────────────────────────────────────────

class SendInviteResponse(BaseModel):
    schedule_id: int
    email_sent: bool
    sms_sent: bool
    available_slots: List[str]
    confirmation_token: str
    message: str


class ConfirmScheduleRequest(BaseModel):
    confirmation_token: str
    selected_slot: str  # ISO 8601 datetime string


class ScheduleOut(BaseModel):
    id: int
    application_id: int
    invite_sent_at: Optional[datetime]
    available_slots: Optional[str]
    confirmed_slot: Optional[datetime]
    is_confirmed: bool
    email_sent: bool
    sms_sent: bool

    model_config = {"from_attributes": True}


# ── Interview ─────────────────────────────────────────────────────────────────

class StartInterviewResponse(BaseModel):
    call_sid: Optional[str]
    message: str
    is_mock: bool


class InterviewResultOut(BaseModel):
    id: int
    application_id: int
    call_sid: Optional[str]
    transcript: Optional[str]
    ai_summary: Optional[str]
    score: Optional[float]
    passed: Optional[bool]
    completed_at: datetime
    is_mock: bool

    model_config = {"from_attributes": True}


# ── Dashboard ─────────────────────────────────────────────────────────────────

class DashboardStats(BaseModel):
    total_applications: int
    by_status: dict
    by_platform: dict
    pass_rate: Optional[float]
    avg_review_score: Optional[float]


class ApplicationListItem(BaseModel):
    id: int
    applicant_name: str
    applicant_email: str
    position: str
    source_platform: SourcePlatform
    status: ApplicationStatus
    created_at: datetime
    review_score: Optional[float] = None
    review_passed: Optional[bool] = None

    model_config = {"from_attributes": True}
