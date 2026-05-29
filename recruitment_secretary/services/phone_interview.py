"""
AI phone interview service using Twilio Voice + Claude.

Flow:
  1. POST /interview/start/{id}  → Twilio initiates outbound call
  2. Twilio calls POST /interview/webhook/voice  (TwiML: greet + first question)
  3. Candidate answers → Gather callback → store answer, ask next question
  4. After all questions → hang up, run AI summary
"""
import os
import json
from typing import List, Optional

INTERVIEW_QUESTIONS: List[str] = [
    "간단하게 자기소개를 해주시겠어요?",
    "지원하신 직무에 관심을 가지게 된 계기는 무엇인가요?",
    "본인의 가장 큰 강점과 그것을 발휘한 경험을 말씀해 주세요.",
    "팀 내 갈등 상황을 어떻게 해결하셨는지 사례를 들어 설명해 주세요.",
    "마지막으로 저희 회사에 대해 궁금한 점이 있으신가요?",
]


def _is_configured() -> bool:
    return all([
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN"),
        os.getenv("TWILIO_PHONE_NUMBER"),
        os.getenv("PUBLIC_BASE_URL"),
    ])


async def initiate_call(application_id: int, phone_number: str) -> dict:
    """Place an outbound call to the candidate. Returns call info."""
    if not _is_configured():
        return {
            "call_sid": f"MOCK-CALL-{application_id}",
            "status": "mock",
            "is_mock": True,
        }

    base_url = os.getenv("PUBLIC_BASE_URL")
    twiml_url = f"{base_url}/interview/webhook/voice?application_id={application_id}"

    try:
        from twilio.rest import Client
        client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        call = client.calls.create(
            to=phone_number,
            from_=os.getenv("TWILIO_PHONE_NUMBER"),
            url=twiml_url,
        )
        return {"call_sid": call.sid, "status": call.status, "is_mock": False}
    except Exception as exc:
        return {"call_sid": None, "status": f"error: {exc}", "is_mock": True}


def validate_twilio_signature(url: str, params: dict, signature: str) -> bool:
    """Returns True if signature is valid or auth token not configured (dev mode)."""
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    if not auth_token:
        return True
    try:
        from twilio.request_validator import RequestValidator
        validator = RequestValidator(auth_token)
        return validator.validate(url, params, signature)
    except Exception:
        return False


def build_twiml_question(question: str, gather_action_url: str) -> str:
    """Return TwiML XML that reads a question and gathers speech input."""
    escaped = _xml_escape(question)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Gather input="speech" action="{gather_action_url}" method="POST" speechTimeout="3" language="ko-KR">
    <Say language="ko-KR" voice="Polly.Seoyeon">{escaped}</Say>
  </Gather>
  <Say language="ko-KR" voice="Polly.Seoyeon">답변을 듣지 못했습니다. 잠시 후 다시 연락드리겠습니다.</Say>
</Response>"""


def build_twiml_goodbye() -> str:
    return """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say language="ko-KR" voice="Polly.Seoyeon">
    인터뷰에 응해 주셔서 감사합니다. 검토 후 결과를 안내드리겠습니다. 좋은 하루 되세요.
  </Say>
  <Hangup/>
</Response>"""


def append_transcript(existing: str, question: str, answer: str) -> str:
    """Append a Q&A pair to the JSON transcript string."""
    try:
        pairs = json.loads(existing) if existing else []
    except Exception:
        pairs = []
    pairs.append({"q": question, "a": answer})
    return json.dumps(pairs, ensure_ascii=False)


def format_transcript_for_summary(transcript_json: str) -> str:
    try:
        pairs = json.loads(transcript_json)
        lines = [f"Q: {p['q']}\nA: {p['a']}" for p in pairs]
        return "\n\n".join(lines)
    except Exception:
        return transcript_json


def _xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
    )
