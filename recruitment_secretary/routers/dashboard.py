from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import Application, ReviewResult, ApplicationStatus, SourcePlatform
from schemas import DashboardStats, ApplicationListItem
from auth import require_api_key

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/applications", response_model=List[ApplicationListItem])
async def list_applications(
    status: Optional[ApplicationStatus] = Query(None),
    platform: Optional[SourcePlatform] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    query = db.query(Application)
    if status:
        query = query.filter(Application.status == status)
    if platform:
        query = query.filter(Application.source_platform == platform)
    applications = query.order_by(Application.created_at.desc()).offset(offset).limit(limit).all()

    items = []
    for app in applications:
        review = app.review
        items.append(ApplicationListItem(
            id=app.id,
            applicant_name=app.applicant.name,
            applicant_email=app.applicant.email,
            position=app.position,
            source_platform=app.source_platform,
            status=app.status,
            created_at=app.created_at,
            review_score=review.score if review else None,
            review_passed=review.passed if review else None,
        ))
    return items


@router.get("/stats", response_model=DashboardStats)
async def get_stats(
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    total = db.query(func.count(Application.id)).scalar()

    by_status_rows = (
        db.query(Application.status, func.count(Application.id))
        .group_by(Application.status)
        .all()
    )
    by_status = {row[0].value: row[1] for row in by_status_rows}

    by_platform_rows = (
        db.query(Application.source_platform, func.count(Application.id))
        .group_by(Application.source_platform)
        .all()
    )
    by_platform = {row[0].value: row[1] for row in by_platform_rows}

    reviewed = db.query(ReviewResult).filter(ReviewResult.passed.isnot(None)).all()
    pass_rate = None
    avg_score = None
    if reviewed:
        passed_count = sum(1 for r in reviewed if r.passed)
        pass_rate = round(passed_count / len(reviewed) * 100, 1)
        avg_score = round(sum(r.score for r in reviewed if r.score is not None) / len(reviewed), 1)

    return DashboardStats(
        total_applications=total,
        by_status=by_status,
        by_platform=by_platform,
        pass_rate=pass_rate,
        avg_review_score=avg_score,
    )
