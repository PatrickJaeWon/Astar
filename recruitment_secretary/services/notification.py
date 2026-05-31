import os
import json
import secrets
from datetime import datetime, timedelta, timezone
from typing import List, Optional
import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def _smtp_configured() -> bool:
    return all([
        os.getenv("SMTP_HOST"),
        os.getenv("SMTP_USERNAME"),
        os.getenv("SMTP_PASSWORD"),
    ])


def _sms_configured() -> bool:
    return all([
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN"),
        os.getenv("TWILIO_PHONE_NUMBER"),
    ])


def generate_confirmation_token() -> str:
    return secrets.token_urlsafe(32)


def generate_available_slots(count: int = 3) -> List[str]:
    """Generate candidate time slots starting from next weekday."""
    slots = []
    dt = datetime.now(timezone.utc).replace(hour=10, minute=0, second=0, microsecond=0)
    dt += timedelta(days=1)
    while len(slots) < count:
        if dt.weekday() < 5:  # Mon–Fri
            slots.append(dt.isoformat())
            dt += timedelta(hours=2)
        else:
            dt += timedelta(days=1)
            dt = dt.replace(hour=10, minute=0)
    return slots


async def send_interview_invite_email(
    to_email: str,
    to_name: str,
    position: str,
    available_slots: List[str],
    confirmation_token: str,
) -> bool:
    company_name = os.getenv("COMPANY_NAME", "AstarCorp")
    base_url = os.getenv("PUBLIC_BASE_URL", "http://localhost:8000")
    confirm_url = f"{base_url}/schedule/confirm"

    slots_html = "\n".join(
        f'<li><a href="{confirm_url}?token={confirmation_token}&slot={s}">'
        f'{_fmt_slot(s)}</a></li>'
        for s in available_slots
    )

    html_body = f"""
    <html><body>
    <p>안녕하세요, {to_name}님</p>
    <p><strong>{company_name}</strong> {position} 직무에 지원해 주셔서 감사합니다.<br>
    서류 전형을 통과하셨습니다. 아래 시간 중 전화 인터뷰가 가능한 일정을 선택해 주세요.</p>
    <ul>{slots_html}</ul>
    <p>감사합니다.<br>{company_name} 채용팀</p>
    </body></html>
    """

    if not _smtp_configured():
        print(f"[MOCK EMAIL] To: {to_email} | Subject: {company_name} 전화 인터뷰 일정 안내")
        return False

    from_email = os.getenv("SMTP_FROM_EMAIL", os.getenv("SMTP_USERNAME", ""))
    from_name = os.getenv("SMTP_FROM_NAME", f"{company_name} 채용팀")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"[{company_name}] {position} 전화 인터뷰 일정 안내"
    msg["From"] = f"{from_name} <{from_email}>"
    msg["To"] = to_email
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    use_tls = os.getenv("SMTP_USE_TLS", "false").lower() == "true"
    port = int(os.getenv("SMTP_PORT", "465" if use_tls else "587"))
    try:
        await aiosmtplib.send(
            msg,
            hostname=os.getenv("SMTP_HOST"),
            port=port,
            username=os.getenv("SMTP_USERNAME"),
            password=os.getenv("SMTP_PASSWORD"),
            use_tls=use_tls,
            start_tls=not use_tls,
        )
        return True
    except Exception as exc:
        print(f"[EMAIL ERROR] {exc}")
        return False


async def send_interview_invite_sms(
    to_phone: str,
    to_name: str,
    position: str,
    available_slots: List[str],
    confirmation_token: str,
) -> bool:
    company_name = os.getenv("COMPANY_NAME", "AstarCorp")
    base_url = os.getenv("PUBLIC_BASE_URL", "http://localhost:8000")
    confirm_url = f"{base_url}/schedule/confirm"

    slot_lines = "\n".join(f"• {_fmt_slot(s)}" for s in available_slots[:3])
    body = (
        f"[{company_name}] {to_name}님, {position} 서류 합격을 축하드립니다!\n"
        f"전화 인터뷰 가능 시간:\n{slot_lines}\n"
        f"일정 선택: {confirm_url}?token={confirmation_token}"
    )

    if not _sms_configured():
        print(f"[MOCK SMS] To: {to_phone} | {body[:80]}...")
        return False

    try:
        from twilio.rest import Client
        client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        client.messages.create(
            body=body,
            from_=os.getenv("TWILIO_PHONE_NUMBER"),
            to=to_phone,
        )
        return True
    except Exception as exc:
        print(f"[SMS ERROR] {exc}")
        return False


def _fmt_slot(iso_str: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%Y년 %m월 %d일 %H:%M (KST)")
    except Exception:
        return iso_str
