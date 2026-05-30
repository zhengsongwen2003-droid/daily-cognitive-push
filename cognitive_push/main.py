from __future__ import annotations

import argparse
from datetime import date, datetime
from time import sleep
from typing import Callable, Sequence

from cognitive_push.config import load_config
from cognitive_push.delivery import send_flomo, send_wecom
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
    if existing_record and existing_record.get("wecom_sent") is True and existing_record.get("flomo_sent") is True:
        return

    if existing_record and existing_record.get("content"):
        card = str(existing_record["content"])
        wecom_sent = bool(existing_record.get("wecom_sent"))
        flomo_sent = bool(existing_record.get("flomo_sent"))

        if not wecom_sent:
            wecom_sent = _retry(lambda: send_wecom(config.wecom_webhook_url, card), attempts=3)
        if not flomo_sent:
            flomo_sent = _retry(lambda: send_flomo(config.flomo_webhook_url, card), attempts=3)

        store.add_record(
            DailyRecord(
                date=current_day_text,
                title=str(existing_record.get("title") or extract_title(card)),
                theme=str(existing_record.get("theme") or extract_tag_line(card)),
                content=card,
                wecom_sent=wecom_sent,
                flomo_sent=flomo_sent,
            )
        )
        if not wecom_sent and not flomo_sent:
            raise RuntimeError("企业微信和 flomo 均发送失败，内容已记录到本地状态")
        return

    card = generate_card(config, theme, store.recent_titles())
    quality = validate_card(card, recent_titles=store.recent_titles(), recent_themes=store.recent_themes())
    if not quality.ok:
        card = generate_card(config, theme, store.recent_titles())
        quality = validate_card(card, recent_titles=store.recent_titles(), recent_themes=store.recent_themes())
    if not quality.ok:
        raise RuntimeError("内容质量检查失败: " + "; ".join(quality.errors))

    wecom_sent = _retry(lambda: send_wecom(config.wecom_webhook_url, card), attempts=3)
    flomo_sent = _retry(lambda: send_flomo(config.flomo_webhook_url, card), attempts=3)

    store.add_record(
        DailyRecord(
            date=current_day.isoformat(),
            title=extract_title(card),
            theme=extract_tag_line(card),
            content=card,
            wecom_sent=wecom_sent,
            flomo_sent=flomo_sent,
        )
    )

    if not wecom_sent and not flomo_sent:
        raise RuntimeError("企业微信和 flomo 均发送失败，内容已记录到本地状态")


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Send one daily cognitive card to WeCom and flomo.")
    parser.add_argument("--force", action="store_true", help="Run immediately, ignoring the configured send hour.")
    args = parser.parse_args(argv)
    run_once(enforce_send_hour=not args.force)


if __name__ == "__main__":
    main()
