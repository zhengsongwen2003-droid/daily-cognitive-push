from __future__ import annotations

import json
import urllib.error
import urllib.request


def _post_json(url: str, payload: dict[str, object], timeout: int = 30) -> dict[str, object]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {error.code}: {body}") from error


def send_pushplus(token: str, content: str) -> None:
    payload = {
        "token": token,
        "title": "每日认知",
        "content": content,
        "template": "markdown",
    }
    result = _post_json("https://www.pushplus.plus/send", payload)
    if result.get("code", 200) != 200:
        raise RuntimeError(f"pushplus send failed: {result}")


def send_flomo(webhook_url: str, content: str) -> None:
    payload = {"content": content}
    result = _post_json(webhook_url, payload)
    if result.get("errcode", 0) != 0 or result.get("code", 0) != 0:
        raise RuntimeError(f"flomo send failed: {result}")
