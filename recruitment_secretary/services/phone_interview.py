"""
AI phone interview service using VAPI (Voice AI Platform).

Flow:
  1. POST /interview/start/{id}  → VAPI outbound call API
  2. VAPI manages the full conversation (STT → Claude → TTS) internally
  3. On call end, VAPI POSTs end-of-call-report to POST /interview/webhook/vapi
  4. Webhook saves transcript + triggers AI summary
"""
import os
import httpx
from typing import Optional

VAPI_BASE_URL = "https://api.vapi.ai"

INTERVIEW_SYSTEM_PROMPT = """\
당신은 {company_name}의 전문 채용 AI 면접관입니다. {position} 직무 지원자와 전화 인터뷰를 진행합니다.

다음 5가지 질문을 순서대로 자연스럽게 물어보세요:
1. 간단하게 자기소개를 해주시겠어요?
2. {position} 직무에 관심을 가지게 된 계기는 무엇인가요?
3. 본인의 가장 큰 강점과 그것을 발휘한 경험을 말씀해 주세요.
4. 팀 내 갈등 상황을 어떻게 해결하셨는지 사례를 들어 설명해 주세요.
5. 마지막으로 저희 회사에 대해 궁금한 점이 있으신가요?

각 답변에 짧게 호응하고 자연스럽게 다음 질문으로 넘어가세요.
모든 질문이 끝나면 인터뷰를 정중히 마무리하고 통화를 종료하세요.
반드시 한국어로만 대화하세요.\
"""


def _is_configured() -> bool:
    return all([
        os.getenv("VAPI_API_KEY"),
        os.getenv("VAPI_PHONE_NUMBER_ID"),
        os.getenv("PUBLIC_BASE_URL"),
    ])


async def initiate_call(application_id: int, phone_number: str, position: str) -> dict:
    """Place an outbound VAPI call. Returns call info dict."""
    if not _is_configured():
        return {
            "call_id": f"MOCK-VAPI-CALL-{application_id}",
            "status": "mock",
            "is_mock": True,
        }

    company_name = os.getenv("COMPANY_NAME", "AstarCorp")
    base_url = os.getenv("PUBLIC_BASE_URL", "")
    webhook_secret = os.getenv("VAPI_WEBHOOK_SECRET", "")

    assistant = {
        "name": f"{company_name} 채용 AI 면접관",
        "firstMessage": (
            f"안녕하세요, {company_name} {position} 채용 면접관입니다. "
            "오늘 시간 내주셔서 감사합니다. 간단한 전화 인터뷰 진행하겠습니다."
        ),
        "endCallMessage": "인터뷰에 응해 주셔서 감사합니다. 검토 후 결과를 안내드리겠습니다. 좋은 하루 보내세요.",
        "model": {
            "provider": "anthropic",
            "model": "claude-sonnet-4-6",
            "systemPrompt": INTERVIEW_SYSTEM_PROMPT.format(
                company_name=company_name,
                position=position,
            ),
            "temperature": 0.6,
        },
        "voice": {
            "provider": "azure",
            "voiceId": "ko-KR-SunHiNeural",
        },
        "serverUrl": f"{base_url}/interview/webhook/vapi",
        **({"serverUrlSecret": webhook_secret} if webhook_secret else {}),
    }

    payload = {
        "phoneNumberId": os.getenv("VAPI_PHONE_NUMBER_ID"),
        "customer": {"number": phone_number},
        "assistant": assistant,
        "metadata": {"application_id": application_id},
    }

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                f"{VAPI_BASE_URL}/call",
                json=payload,
                headers={"Authorization": f"Bearer {os.getenv('VAPI_API_KEY')}"},
            )
            resp.raise_for_status()
            data = resp.json()
            return {
                "call_id": data.get("id"),
                "status": data.get("status"),
                "is_mock": False,
            }
    except Exception as exc:
        return {"call_id": None, "status": f"error: {exc}", "is_mock": True}


def validate_webhook_secret(request_secret: Optional[str]) -> bool:
    """Returns True if secret matches or no secret is configured (dev mode)."""
    expected = os.getenv("VAPI_WEBHOOK_SECRET")
    if not expected:
        return True
    return request_secret == expected


def parse_end_of_call_report(payload: dict) -> Optional[dict]:
    """
    Extract transcript, summary, call_id from a VAPI end-of-call-report webhook.
    Returns None if payload is not this event type.
    """
    message = payload.get("message", {})
    if message.get("type") != "end-of-call-report":
        return None

    call = message.get("call", {})
    return {
        "call_id": call.get("id"),
        "application_id": (call.get("metadata") or {}).get("application_id"),
        "transcript": message.get("transcript", ""),
        "vapi_summary": message.get("summary", ""),
        "recording_url": message.get("recordingUrl"),
        "ended_reason": call.get("endedReason"),
    }
