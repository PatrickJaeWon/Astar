from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum
from database import Base


class ApplicationStatus(str, enum.Enum):
    RECEIVED = "received"
    REVIEWING = "reviewing"
    PASSED = "passed"
    FAILED = "failed"
    INTERVIEW_INVITED = "interview_invited"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEW_DONE = "interview_done"
    HIRED = "hired"
    REJECTED = "rejected"


class SourcePlatform(str, enum.Enum):
    WANTED = "wanted"
    REMEMBER = "remember"
    GROUPBY = "groupby"
    EMAIL = "email"
    MANUAL = "manual"


class Applicant(Base):
    __tablename__ = "applicants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False, index=True)
    phone = Column(String(30))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    applications = relationship("Application", back_populates="applicant")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(Integer, ForeignKey("applicants.id"), nullable=False)
    position = Column(String(200), nullable=False)
    source_platform = Column(SAEnum(SourcePlatform), nullable=False)
    external_id = Column(String(200))  # platform-specific application ID
    resume_text = Column(Text)
    cover_letter = Column(Text)
    resume_url = Column(String(500))
    status = Column(SAEnum(ApplicationStatus), default=ApplicationStatus.RECEIVED)
    raw_payload = Column(Text)  # original webhook payload for debugging
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    applicant = relationship("Applicant", back_populates="applications")
    review = relationship("ReviewResult", back_populates="application", uselist=False)
    schedule = relationship("InterviewSchedule", back_populates="application", uselist=False)
    interview_result = relationship("InterviewResult", back_populates="application", uselist=False)
    interview_session = relationship("InterviewSession", back_populates="application", uselist=False)


class ReviewResult(Base):
    __tablename__ = "review_results"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False, unique=True)
    score = Column(Float)  # 0-100
    passed = Column(Boolean)
    summary = Column(Text)
    strengths = Column(Text)
    weaknesses = Column(Text)
    recommendation = Column(Text)
    reviewed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_mock = Column(Boolean, default=False)

    application = relationship("Application", back_populates="review")


class InterviewSchedule(Base):
    __tablename__ = "interview_schedules"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False, unique=True)
    invite_sent_at = Column(DateTime)
    available_slots = Column(Text)  # JSON: list of proposed datetime strings
    confirmed_slot = Column(DateTime)
    confirmation_token = Column(String(64), unique=True, index=True)
    email_sent = Column(Boolean, default=False)
    sms_sent = Column(Boolean, default=False)
    is_confirmed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    application = relationship("Application", back_populates="schedule")


class InterviewSession(Base):
    """Tracks stateful conversation during an AI phone interview (per TwiML callback)."""
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False, unique=True)
    call_sid = Column(String(64), index=True)
    current_question_index = Column(Integer, default=0)
    transcript = Column(Text, default="")  # accumulated Q&A pairs as JSON
    is_complete = Column(Boolean, default=False)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    application = relationship("Application", back_populates="interview_session")


class InterviewResult(Base):
    __tablename__ = "interview_results"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False, unique=True)
    call_sid = Column(String(64))
    transcript = Column(Text)
    ai_summary = Column(Text)
    score = Column(Float)
    passed = Column(Boolean)
    completed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_mock = Column(Boolean, default=False)

    application = relationship("Application", back_populates="interview_result")
