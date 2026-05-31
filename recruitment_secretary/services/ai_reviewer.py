import os
import json
from typing import Optional

_client = None


def _is_configured() -> bool:
    return bool(os.getenv("ANTHROPIC_API_KEY"))


def _get_client():
    global _client
    if _client is None:
        import anthropic
        _client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    return _client


REVIEW_SYSTEM_PROMPT = """당신은 전문 채용 담당자입니다. 지원자의 이력서와 자기소개서를 분석하여 직무 적합성을 평가합니다.
다음 JSON 형식으로만 응답하세요:
{
  "score": <0-100 사이의 숫자>,
  "passed": <true/false — 70점 이상이면 true>,
  "summary": "<200자 이내 종합 평가>",
  "strengths": "<핵심 강점 3가지 이내, 줄바꿈으로 구분>",
  "weaknesses": "<개선 필요 사항 2가지 이내, 줄바꿈으로 구분>",
  "recommendation": "<합격/불합격 사유와 다음 단계 권고>"
}"""


async def review_application(
    position: str,
    resume_text: Optional[str],
    cover_letter: Optional[str],
) -> dict:
    """Returns review dict. Falls back to mock if API key not set."""
    if not _is_configured():
        return _mock_review(position)

    content_parts = [f"지원 직무: {position}"]
    if resume_text:
        content_parts.append(f"\n## 이력서\n{resume_text}")
    if cover_letter:
        content_parts.append(f"\n## 자기소개서\n{cover_letter}")

    user_message = "\n".join(content_parts)

    try:
        client = _get_client()
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=REVIEW_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )
        raw = response.content[0].text.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        result = json.loads(raw)
        result["is_mock"] = False
        return result
    except Exception as exc:
        return _mock_review(position, error=str(exc))


def _mock_review(position: str, error: str = "") -> dict:
    note = f" [MOCK — 오류: {error}]" if error else " [MOCK — API 키 미설정]"
    return {
        "score": 72.0,
        "passed": True,
        "summary": f"{position} 직무에 대한 모의 평가입니다.{note}",
        "strengths": "관련 경험 보유\n커뮤니케이션 능력\n빠른 학습 능력",
        "weaknesses": "실무 경력 부족\n기술 스택 일부 미달",
        "recommendation": "서류 합격 — 전화 인터뷰를 통해 추가 검증 권고",
        "is_mock": True,
    }


INTERVIEW_SUMMARY_PROMPT = """당신은 채용 담당자입니다. 아래 전화 인터뷰 대화록을 분석하고 JSON으로 요약하세요:
{
  "score": <0-100>,
  "passed": <true/false — 65점 이상이면 true>,
  "ai_summary": "<300자 이내 인터뷰 종합 평가>",
}"""


async def summarize_interview(transcript: str, position: str) -> dict:
    """Summarize completed phone interview transcript."""
    if not _is_configured():
        return {
            "score": 68.0,
            "passed": True,
            "ai_summary": f"[MOCK] {position} 전화 인터뷰 요약. API 키가 설정되지 않아 모의 결과를 반환합니다.",
            "is_mock": True,
        }

    try:
        client = _get_client()
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=512,
            system=INTERVIEW_SUMMARY_PROMPT,
            messages=[
                {"role": "user", "content": f"직무: {position}\n\n대화록:\n{transcript}"}
            ],
        )
        raw = response.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        result = json.loads(raw)
        result["is_mock"] = False
        return result
    except Exception as exc:
        return {
            "score": 68.0,
            "passed": True,
            "ai_summary": f"요약 생성 오류: {exc}",
            "is_mock": True,
        }
