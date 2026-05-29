from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Application, ReviewResult, ApplicationStatus
from schemas import ReviewResultOut
from services.ai_reviewer import review_application
from auth import require_api_key

router = APIRouter(prefix="/review", tags=["review"])


@router.post("/{application_id}", response_model=ReviewResultOut)
async def run_review(
    application_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="지원서를 찾을 수 없습니다.")

    if application.review:
        raise HTTPException(status_code=409, detail="이미 심사가 완료된 지원서입니다.")

    application.status = ApplicationStatus.REVIEWING
    db.commit()

    result = await review_application(
        position=application.position,
        resume_text=application.resume_text,
        cover_letter=application.cover_letter,
    )

    review = ReviewResult(
        application_id=application.id,
        score=result.get("score"),
        passed=result.get("passed"),
        summary=result.get("summary"),
        strengths=result.get("strengths"),
        weaknesses=result.get("weaknesses"),
        recommendation=result.get("recommendation"),
        is_mock=result.get("is_mock", False),
    )
    db.add(review)

    application.status = ApplicationStatus.PASSED if result.get("passed") else ApplicationStatus.FAILED
    db.commit()
    db.refresh(review)
    return review


@router.get("/{application_id}", response_model=ReviewResultOut)
async def get_review(
    application_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    review = db.query(ReviewResult).filter(ReviewResult.application_id == application_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="심사 결과가 없습니다. 먼저 POST /review/{id}를 호출하세요.")
    return review
