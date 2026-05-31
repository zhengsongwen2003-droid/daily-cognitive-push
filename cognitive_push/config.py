from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    deepseek_api_key: str
    deepseek_model: str
    pushplus_token: str
    state_path: str
    send_hour: int


@dataclass(frozen=True)
class AppConfig:
    database_path: str
    api_host: str
    api_port: int
    apns_team_id: str
    apns_key_id: str
    apns_bundle_id: str
    apns_auth_token: str
    apns_private_key_path: str
    apns_environment: str


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
        deepseek_api_key=_required_env("DEEPSEEK_API_KEY"),
        deepseek_model=os.environ.get("DEEPSEEK_MODEL", "deepseek-chat").strip() or "deepseek-chat",
        pushplus_token=_required_env("PUSHPLUS_TOKEN"),
        state_path=os.environ.get("COGNITIVE_PUSH_STATE", "data/state.json").strip() or "data/state.json",
        send_hour=send_hour,
    )


def load_app_config() -> AppConfig:
    api_port = int(os.environ.get("COGNITIVE_PUSH_API_PORT", "8080"))
    if api_port < 1 or api_port > 65535:
        raise RuntimeError("COGNITIVE_PUSH_API_PORT must be between 1 and 65535")

    return AppConfig(
        database_path=os.environ.get("COGNITIVE_PUSH_DATABASE", "data/app.sqlite3").strip() or "data/app.sqlite3",
        api_host=os.environ.get("COGNITIVE_PUSH_API_HOST", "127.0.0.1").strip() or "127.0.0.1",
        api_port=api_port,
        apns_team_id=os.environ.get("APNS_TEAM_ID", "").strip(),
        apns_key_id=os.environ.get("APNS_KEY_ID", "").strip(),
        apns_bundle_id=os.environ.get("APNS_BUNDLE_ID", "").strip(),
        apns_auth_token=os.environ.get("APNS_AUTH_TOKEN", "").strip(),
        apns_private_key_path=os.environ.get("APNS_PRIVATE_KEY_PATH", "").strip(),
        apns_environment=os.environ.get("APNS_ENVIRONMENT", "sandbox").strip() or "sandbox",
    )


def load_generation_config() -> Config:
    send_hour = int(os.environ.get("COGNITIVE_PUSH_SEND_HOUR", "8"))
    if send_hour < 0 or send_hour > 23:
        raise RuntimeError("COGNITIVE_PUSH_SEND_HOUR must be between 0 and 23")

    return Config(
        deepseek_api_key=_required_env("DEEPSEEK_API_KEY"),
        deepseek_model=os.environ.get("DEEPSEEK_MODEL", "deepseek-chat").strip() or "deepseek-chat",
        pushplus_token=os.environ.get("PUSHPLUS_TOKEN", "").strip(),
        state_path=os.environ.get("COGNITIVE_PUSH_STATE", "data/state.json").strip() or "data/state.json",
        send_hour=send_hour,
    )
