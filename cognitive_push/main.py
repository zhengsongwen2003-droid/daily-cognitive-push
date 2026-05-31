from __future__ import annotations

import argparse
from datetime import date, datetime
from time import sleep
from typing import Callable, Sequence

from cognitive_push.config import load_app_config, load_config, load_generation_config
from cognitive_push.delivery import send_pushplus
from cognitive_push.generator import generate_card
from cognitive_push.quality import extract_tag_line, extract_title, validate_card
from cognitive_push.state import DailyRecord, StateStore
from cognitive_push.themes import theme_for_date


def _retry(action: Callable[[], None], attempts: int = 3, delay_seconds: int = 3) -> bool:
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            action()
            return True
        except Exception as error:
            last_error = error
            if attempt < attempts - 1:
                sleep(delay_seconds)
    print(f"发送失败: {last_error}")
    return False


def should_send_at(now: datetime, send_hour: int) -> bool:
    return now.hour == send_hour


def run_once(today: date | None = None, enforce_send_hour: bool = False, now: datetime | None = None) -> None:
    config = load_config()
    current_time = now or datetime.now()
    if enforce_send_hour and not should_send_at(current_time, config.send_hour):
        print(f"当前不是配置的推送时间 {config.send_hour}:00，已跳过。")
        return

    current_day = today or current_time.date()
    theme = theme_for_date(current_day)
    store = StateStore(config.state_path)
    current_day_text = current_day.isoformat()
    existing_record = store.latest_record_for_date(current_day_text)
    existing_pushplus_sent = bool(existing_record and existing_record.get("pushplus_sent", existing_record.get("wecom_sent", False)))
    if existing_record and existing_pushplus_sent is True:
        return

    if existing_record and existing_record.get("content"):
        card = str(existing_record["content"])
        pushplus_sent = bool(existing_record.get("pushplus_sent", existing_record.get("wecom_sent", False)))

        if not pushplus_sent:
            pushplus_sent = _retry(lambda: send_pushplus(config.pushplus_token, card), attempts=3)

        store.add_record(
            DailyRecord(
                date=current_day_text,
                title=str(existing_record.get("title") or extract_title(card)),
                theme=str(existing_record.get("theme") or extract_tag_line(card)),
                content=card,
                pushplus_sent=pushplus_sent,
            )
        )
        if not pushplus_sent:
            raise RuntimeError("pushplus 发送失败，内容已记录到本地状态")
        return

    card = generate_card(config, theme, store.recent_titles())
    quality = validate_card(card, recent_titles=store.recent_titles(), recent_themes=store.recent_themes())
    if not quality.ok:
        card = generate_card(config, theme, store.recent_titles())
        quality = validate_card(card, recent_titles=store.recent_titles(), recent_themes=store.recent_themes())
    if not quality.ok:
        raise RuntimeError("内容质量检查失败: " + "; ".join(quality.errors))

    pushplus_sent = _retry(lambda: send_pushplus(config.pushplus_token, card), attempts=3)

    store.add_record(
        DailyRecord(
            date=current_day.isoformat(),
            title=extract_title(card),
            theme=extract_tag_line(card),
            content=card,
            pushplus_sent=pushplus_sent,
        )
    )

    if not pushplus_sent:
        raise RuntimeError("pushplus 发送失败，内容已记录到本地状态")


def _build_app_service():
    from cognitive_push.app_service import CognitiveAppService
    from cognitive_push.app_store import AppStore

    app_config = load_app_config()
    push_config = load_generation_config()

    def card_generator(day: date) -> str:
        theme = theme_for_date(day)
        store = AppStore(app_config.database_path)
        return generate_card(push_config, theme, store.recent_titles())

    return CognitiveAppService(AppStore(app_config.database_path), card_generator=card_generator)


def serve_app_api() -> None:
    from cognitive_push.api import AppAPI, run_server

    app_config = load_app_config()
    run_server(AppAPI(_build_app_service()), host=app_config.api_host, port=app_config.api_port)


def run_ios_notification_once(today: date | None = None) -> None:
    from cognitive_push.apns import APNSClient, APNSConfig
    from cognitive_push.scheduler import send_daily_card_notifications

    app_config = load_app_config()
    service = _build_app_service()
    apns = APNSClient(
        APNSConfig(
            team_id=app_config.apns_team_id,
            key_id=app_config.apns_key_id,
            bundle_id=app_config.apns_bundle_id,
            auth_token=app_config.apns_auth_token,
            private_key_path=app_config.apns_private_key_path,
            environment=app_config.apns_environment,
        )
    )
    send_daily_card_notifications(
        service,
        today or date.today(),
        lambda token, card_id, title: apns.send_card_notification(token, card_id, title),
    )


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Send one daily cognitive card to pushplus.")
    parser.add_argument("--force", action="store_true", help="Run immediately, ignoring the configured send hour.")
    parser.add_argument("--serve-api", action="store_true", help="Run the iOS app HTTP API server.")
    parser.add_argument("--send-ios-notification", action="store_true", help="Generate today's card and send APNs notifications.")
    args = parser.parse_args(argv)
    if args.serve_api:
        serve_app_api()
        return
    if args.send_ios_notification:
        run_ios_notification_once()
        return
    run_once(enforce_send_hour=not args.force)


if __name__ == "__main__":
    main()
