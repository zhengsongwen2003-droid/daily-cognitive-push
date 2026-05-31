from __future__ import annotations

import re
from dataclasses import dataclass


REQUIRED_SECTIONS = ("1. 案例", "2. 关键转折", "3. 认知模型", "4. 常见误判", "5. 迁移到你", "6. 今日一问", "7. 微行动")
SECTION_PATTERN = re.compile(r"(?m)^\*{0,2}(?P<number>[1-7])\.\s+\*{0,2}(?P<name>[^\n*]+?)\*{0,2}\s*$")


@dataclass(frozen=True)
class QualityResult:
    ok: bool
    errors: list[str]


def extract_title(card: str) -> str:
    match = re.search(r"^\*{0,2}标题[:：]\s*(.+?)\*{0,2}\s*$", card, flags=re.MULTILINE)
    return match.group(1).strip().rstrip("*").strip() if match else ""


def extract_tag_line(card: str) -> str:
    for line in card.splitlines():
        if line.startswith("#每日认知"):
            return line.strip()
    return ""


def _section_bodies(card: str) -> dict[str, str]:
    matches = list(SECTION_PATTERN.finditer(card))
    headers = [f"{match.group('number')}. {match.group('name').strip()}" for match in matches]
    if headers != list(REQUIRED_SECTIONS):
        return {}

    bodies: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(card)
        header = f"{match.group('number')}. {match.group('name').strip()}"
        bodies[header] = card[start:end].strip()
    return bodies


def validate_card(card: str, recent_titles: set[str], recent_themes: set[str]) -> QualityResult:
    errors: list[str] = []
    title = extract_title(card)
    tag_line = extract_tag_line(card)
    section_headers = [f"{match.group('number')}. {match.group('name').strip()}" for match in SECTION_PATTERN.finditer(card)]

    if not title:
        errors.append("缺少标题")
    if title in recent_titles:
        errors.append("标题最近 30 天内已出现")
    if not tag_line:
        errors.append("缺少 #每日认知 标签")
    elif tag_line in {"#每日认知", "#每日认知/"} or "/" not in tag_line or not tag_line.split("/", 1)[1].strip():
        errors.append("主题标签不完整")

    section_bodies = _section_bodies(card)
    missing_sections = [section for section in REQUIRED_SECTIONS if section not in section_headers]
    if section_headers and section_headers != list(REQUIRED_SECTIONS):
        errors.append("章节顺序或数量不正确")
    if missing_sections:
        errors.append(f"缺少章节: {', '.join(missing_sections)}")
    elif not section_bodies and "章节顺序或数量不正确" not in errors:
        errors.append("章节顺序或数量不正确")
    else:
        empty_sections = [section for section, body in section_bodies.items() if not body]
        if empty_sections:
            errors.append(f"章节内容为空: {', '.join(empty_sections)}")

    question_body = section_bodies.get("6. 今日一问", "")
    if "今日一问" in card and "？" not in question_body and "?" not in question_body:
        errors.append("今日一问必须包含问题")

    action_body = section_bodies.get("7. 微行动", "")
    if "10 分钟" not in action_body and "10分钟" not in action_body and "十分钟" not in action_body:
        errors.append("微行动需要明确 10 分钟左右可完成")

    if len(card) < 450:
        errors.append("内容过短，不足以支撑 3-5 分钟阅读")
    if len(card) > 2600:
        errors.append("内容过长，超过 3-5 分钟阅读范围")

    return QualityResult(ok=not errors, errors=errors)
