from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class DailyRecord:
    date: str
    title: str
    theme: str
    content: str
    wecom_sent: bool
    flomo_sent: bool


class StateStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"records": []}
        with self.path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def save(self, data: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def add_record(self, record: DailyRecord) -> None:
        data = self.load()
        records = [*data.get("records", []), asdict(record)]
        data["records"] = records[-30:]
        self.save(data)

    def recent_titles(self) -> set[str]:
        return {item["title"] for item in self.load().get("records", [])}

    def recent_themes(self) -> set[str]:
        return {item["theme"] for item in self.load().get("records", [])}

    def has_successful_record_for_date(self, date_value: str) -> bool:
        return any(
            item.get("date") == date_value and item.get("wecom_sent") is True and item.get("flomo_sent") is True
            for item in self.load().get("records", [])
        )

    def latest_record_for_date(self, date_value: str) -> dict[str, Any] | None:
        matches = [item for item in self.load().get("records", []) if item.get("date") == date_value]
        return matches[-1] if matches else None
