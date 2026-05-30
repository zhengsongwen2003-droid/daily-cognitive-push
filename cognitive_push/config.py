from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    openai_api_key: str
    openai_model: str
    wecom_webhook_url: str
    flomo_webhook_url: str
    state_path: str
    send_hour: int


def _required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def load_config() -> Config:
    send_hour = int(os.environ.get("COGNITIVE_PUSH_SEND_HOUR", "8"))
    if send_hour < 0 or send_hour > 23:
        raise RuntimeError("COGNITIVE_PUSH_SEND_HOUR must be between 0 and 23")

    return Config(
        openai_api_key=_required_env("OPENAI_API_KEY"),
        openai_model=os.environ.get("OPENAI_MODEL", "gpt-5").strip() or "gpt-5",
        wecom_webhook_url=_required_env("WECOM_WEBHOOK_URL"),
        flomo_webhook_url=_required_env("FLOMO_WEBHOOK_URL"),
        state_path=os.environ.get("COGNITIVE_PUSH_STATE", "data/state.json").strip() or "data/state.json",
        send_hour=send_hour,
    )
