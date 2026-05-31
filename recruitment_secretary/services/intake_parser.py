"""
Platform-specific webhook payload parsing.
Each function returns a normalized dict with keys:
  name, email, phone, position, resume_url, cover_letter, external_id
"""
from typing import Any, Dict


def parse_wanted(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "name": payload["applicant_name"],
        "email": payload["applicant_email"],
        "phone": payload.get("applicant_phone"),
        "position": payload["job_title"],
        "resume_url": payload.get("resume_url"),
        "cover_letter": payload.get("cover_letter"),
        "external_id": str(payload["application_id"]),
    }


def parse_remember(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "name": payload["name"],
        "email": payload["email"],
        "phone": payload.get("mobile"),
        "position": payload["position"],
        "resume_url": payload.get("profile_url"),
        "cover_letter": payload.get("introduction"),
        "external_id": str(payload["id"]),
    }


def parse_groupby(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "name": payload["user_name"],
        "email": payload["user_email"],
        "phone": payload.get("user_phone"),
        "position": payload["job_name"],
        "resume_url": payload.get("resume_link"),
        "cover_letter": payload.get("self_introduction"),
        "external_id": str(payload["apply_no"]),
    }


def parse_email(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "name": payload["sender_name"],
        "email": payload["sender_email"],
        "phone": payload.get("sender_phone"),
        "position": payload["position"],
        "resume_url": None,
        "cover_letter": payload.get("cover_letter"),
        "external_id": None,
    }
