"""Safe, optional Angular-in-Streamlit bridge (read-only PoC).

This module does not write to Google Sheets. Production workflows remain native.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

BUILD_DIR = Path(__file__).resolve().parent / "frontend" / "dist" / "timetable-angular" / "browser"
ALLOWED_COLS = ("교사명", "요일", "교시", "과목", "학급")
EVENT_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_:-]{8,96}$")


def preview_rows(timetable: Any, limit: int = 120) -> list[dict[str, str]]:
    """Return only necessary columns, never secrets, for authorized preview."""
    if timetable is None or not hasattr(timetable, "columns"):
        return []
    cols = [c for c in ALLOWED_COLS if c in timetable.columns]
    if not cols or "교사명" not in cols:
        return []
    result = []
    for row in timetable.loc[:, cols].head(limit).to_dict("records"):
        item = {}
        for c, value in row.items():
            # pandas NaN/null handling without coercing it to literal 'nan'.
            item[c] = "" if value is None or str(value).lower() in ("nan", "nat") else str(value)[:180]
        result.append(item)
    return result


def validate_nav_event(event: Any, allowed_tabs: list[str]) -> tuple[str, str] | None:
    """Validate untrusted browser messages. No arbitrary commands or writes."""
    if not isinstance(event, dict) or set(event) != {"type", "target", "id"}:
        return None
    if event.get("type") != "navigate":
        return None
    target = event.get("target")
    event_id = event.get("id")
    if not isinstance(target, str) or target not in allowed_tabs:
        return None
    if not isinstance(event_id, str) or not EVENT_ID_PATTERN.fullmatch(event_id):
        return None
    return (event_id, target)


def consume_nav_event(event: Any, allowed_tabs: list[str], already_processed: list[str]) -> str | None:
    validated = validate_nav_event(event, allowed_tabs)
    if validated is None:
        return None
    event_id, target = validated
    if event_id in already_processed:
        return None
    already_processed.append(event_id)
    if len(already_processed) > 80:
        del already_processed[:-80]
    return target


def render_angular_preview(*, session_state: Any, allowed_tabs: list[str],
                           user_label: str, role_label: str, timetable: Any) -> str | None:
    import streamlit as st
    import streamlit.components.v1 as components

    if not (BUILD_DIR / "index.html").is_file():
        st.caption("Angular 미리보기 비활성: 빌드 파일이 없습니다. 기존 시간표 기능은 그대로 사용합니다.")
        return None
    if not allowed_tabs:
        return None
    # Restrict preview timetable data to users who can view this legacy tab.
    rows = preview_rows(timetable) if "시간표 조회" in allowed_tabs else []
    payload = {
        "tabs": list(allowed_tabs),
        "currentTab": str(session_state.get("active_tab", "")),
        "user": user_label[:100],
        "role": role_label[:80],
        "rows": rows,
        "mode": "READ_ONLY_PREVIEW",
    }
    component = components.declare_component("timetable_angular_safe_preview", path=str(BUILD_DIR))
    incoming = component(payload=payload, key="timetable_angular_safe_preview", default=None, height=560)
    processed = session_state.setdefault("_angular_processed_events", [])
    return consume_nav_event(incoming, list(allowed_tabs), processed)
