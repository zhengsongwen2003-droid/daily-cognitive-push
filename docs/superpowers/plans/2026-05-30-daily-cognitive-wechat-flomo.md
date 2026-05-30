# 每日认知微信 + flomo 推送系统 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个每天 08:00 自动生成 3-5 分钟认知案例、推送到企业微信机器人、并同步保存到 flomo 的最小可运行系统。

**Architecture:** 使用一个轻量 Python 命令行应用。配置从环境变量读取，状态写入本地 JSON 文件，主流程按“选择主题 -> 生成内容 -> 校验内容 -> 发送企业微信 -> 保存 flomo -> 记录状态”执行。

**Tech Stack:** Python 3.11+、标准库 `urllib.request`、标准库 `json`、标准库 `unittest`、OpenAI Responses API、Windows 任务计划程序或等价 cron。

---

## 文件结构

- Create: `cognitive_push/__init__.py`  
  包标记文件。
- Create: `cognitive_push/config.py`  
  读取和校验环境变量。
- Create: `cognitive_push/state.py`  
  读写最近 30 天标题、主题标签和发送结果。
- Create: `cognitive_push/themes.py`  
  按星期选择每日主题。
- Create: `cognitive_push/generator.py`  
  调用 OpenAI Responses API 生成认知卡片。
- Create: `cognitive_push/quality.py`  
  检查 7 段结构、长度、标题重复度和关键字段。
- Create: `cognitive_push/delivery.py`  
  发送企业微信机器人和 flomo webhook。
- Create: `cognitive_push/main.py`  
  编排完整每日流程。
- Create: `tests/test_themes.py`  
  测试星期到主题的映射。
- Create: `tests/test_quality.py`  
  测试内容质量检查。
- Create: `tests/test_state.py`  
  测试状态读写和最近 30 天裁剪。
- Create: `README.md`  
  记录配置、运行和定时任务设置。
- Create: `.env.example`  
  展示需要配置的环境变量名称，不写真实密钥。

## 参考资料

- OpenAI Responses API：官方文档说明 Responses 是新项目推荐接口，并支持文本生成。
- 企业微信机器人：使用机器人 webhook 接收 JSON 文本消息。
- flomo：使用已获取的 flomo API 或 incoming webhook 地址保存内容。

## Task 1: 项目骨架和配置读取

**Files:**
- Create: `cognitive_push/__init__.py`
- Create: `cognitive_push/config.py`
- Create: `.env.example`

- [ ] **Step 1: 创建包目录和测试目录**

Run:

```powershell
New-Item -ItemType Directory -Path cognitive_push -Force
New-Item -ItemType Directory -Path tests -Force
```

Expected: 两个目录存在。

- [ ] **Step 2: 创建包标记文件**

Create `cognitive_push/__init__.py`:

```python
"""Daily cognitive push automation."""
```

- [ ] **Step 3: 写配置读取代码**

Create `cognitive_push/config.py`:

```python
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
```

- [ ] **Step 4: 创建环境变量示例**

Create `.env.example`:

```text
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-5
WECOM_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-key
FLOMO_WEBHOOK_URL=https://flomoapp.com/iwh/your-token
COGNITIVE_PUSH_STATE=data/state.json
COGNITIVE_PUSH_SEND_HOUR=8
```

- [ ] **Step 5: 验证配置缺失时会报错**

Run:

```powershell
python -m cognitive_push.config
```

Expected: 没有输出也可以，因为该模块没有入口函数。配置读取会在后续测试中验证。

## Task 2: 主题轮换

**Files:**
- Create: `cognitive_push/themes.py`
- Create: `tests/test_themes.py`

- [ ] **Step 1: 写失败测试**

Create `tests/test_themes.py`:

```python
from datetime import date

from cognitive_push.themes import theme_for_date


def test_theme_for_monday():
    theme = theme_for_date(date(2026, 6, 1))
    assert theme.name == "决策偏误"
    assert "确认偏误" in theme.examples


def test_theme_for_sunday_is_review():
    theme = theme_for_date(date(2026, 6, 7))
    assert theme.name == "本周复盘"
    assert theme.is_review is True
```

- [ ] **Step 2: 运行测试确认失败**

Run:

```powershell
python -m unittest tests.test_themes -v
```

Expected: FAIL，提示找不到 `cognitive_push.themes`。

- [ ] **Step 3: 实现主题模块**

Create `cognitive_push/themes.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Theme:
    name: str
    description: str
    examples: tuple[str, ...]
    is_review: bool = False


THEMES: dict[int, Theme] = {
    0: Theme("决策偏误", "训练识别常见误判和错误决策路径。", ("确认偏误", "沉没成本", "过度自信")),
    1: Theme("长期主义与复利", "训练长期收益、耐心和机会成本意识。", ("复利", "机会成本", "延迟满足")),
    2: Theme("人性与关系", "训练理解关系、动机和边界。", ("损失厌恶", "投射效应", "互惠原则")),
    3: Theme("商业或产品案例", "从商业和产品案例中提炼可迁移判断。", ("激励错位", "用户价值", "二阶思维")),
    4: Theme("职场与管理判断", "训练组织、协作和职业选择判断。", ("代理问题", "路径依赖", "反馈循环")),
    5: Theme("历史、投资或社会案例", "用更大尺度案例训练风险和周期感。", ("周期", "安全边际", "叙事陷阱")),
    6: Theme("本周复盘", "总结一周认知训练并提出下周方向。", ("复盘", "模式识别", "行动校准"), True),
}


def theme_for_date(day: date) -> Theme:
    return THEMES[day.weekday()]
```

- [ ] **Step 4: 运行测试确认通过**

Run:

```powershell
python -m unittest tests.test_themes -v
```

Expected: PASS。

## Task 3: 本地状态记录

**Files:**
- Create: `cognitive_push/state.py`
- Create: `tests/test_state.py`

- [ ] **Step 1: 写失败测试**

Create `tests/test_state.py`:

```python
from cognitive_push.state import DailyRecord, StateStore


def test_state_store_starts_empty(tmp_path):
    store = StateStore(tmp_path / "state.json")
    assert store.recent_titles() == set()
    assert store.recent_themes() == set()


def test_state_store_keeps_last_30_records(tmp_path):
    store = StateStore(tmp_path / "state.json")
    for index in range(35):
        store.add_record(DailyRecord(date=f"2026-06-{index + 1:02d}", title=f"title-{index}", theme=f"theme-{index}", wecom_sent=True, flomo_sent=True))

    data = store.load()
    assert len(data["records"]) == 30
    assert data["records"][0]["title"] == "title-5"
    assert "title-34" in store.recent_titles()
```

- [ ] **Step 2: 运行测试确认失败**

Run:

```powershell
python -m unittest tests.test_state -v
```

Expected: FAIL，提示找不到 `cognitive_push.state`。

- [ ] **Step 3: 实现状态模块**

Create `cognitive_push/state.py`:

```python
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
```

- [ ] **Step 4: 运行测试确认通过**

Run:

```powershell
python -m unittest tests.test_state -v
```

Expected: PASS。

## Task 4: 内容质量检查

**Files:**
- Create: `cognitive_push/quality.py`
- Create: `tests/test_quality.py`

- [ ] **Step 1: 写失败测试**

Create `tests/test_quality.py`:

```python
from cognitive_push.quality import validate_card


VALID_CARD = """#每日认知/认知偏差

标题：为什么聪明人也会拖着错误决定不放？

1. 案例
一个人已经在错误项目上投入很多时间，于是继续投入更多资源。

2. 关键转折
真正的转折点不是项目变好，而是承认损失会带来自尊压力。

3. 认知模型
这背后是沉没成本：已经付出的成本不应该决定下一步选择。

4. 常见误判
很多人会把继续投入理解成负责，其实只是害怕承认之前判断错了。

5. 迁移到你
当你迟迟不愿意停止某件事时，可以先问它未来是否仍然值得。

6. 今日一问
我现在有没有一件事，是因为已经投入太多才继续坚持？

7. 微行动
今天花 10 分钟写下一个正在消耗你的选择，并列出继续和停止的未来收益。
"""


def test_valid_card_passes_quality_check():
    result = validate_card(VALID_CARD, recent_titles=set(), recent_themes=set())
    assert result.ok is True
    assert result.errors == []


def test_missing_section_fails_quality_check():
    result = validate_card("标题：太短", recent_titles=set(), recent_themes=set())
    assert result.ok is False
    assert any("缺少章节" in error for error in result.errors)


def test_repeated_title_fails_quality_check():
    result = validate_card(VALID_CARD, recent_titles={"为什么聪明人也会拖着错误决定不放？"}, recent_themes=set())
    assert result.ok is False
    assert "标题最近 30 天内已出现" in result.errors
```

- [ ] **Step 2: 运行测试确认失败**

Run:

```powershell
python -m unittest tests.test_quality -v
```

Expected: FAIL，提示找不到 `cognitive_push.quality`。

- [ ] **Step 3: 实现质量检查**

Create `cognitive_push/quality.py`:

```python
from __future__ import annotations

import re
from dataclasses import dataclass


REQUIRED_SECTIONS = ("1. 案例", "2. 关键转折", "3. 认知模型", "4. 常见误判", "5. 迁移到你", "6. 今日一问", "7. 微行动")


@dataclass(frozen=True)
class QualityResult:
    ok: bool
    errors: list[str]


def extract_title(card: str) -> str:
    match = re.search(r"^标题[:：]\s*(.+)$", card, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def extract_tag_line(card: str) -> str:
    for line in card.splitlines():
        if line.startswith("#每日认知"):
            return line.strip()
    return ""


def validate_card(card: str, recent_titles: set[str], recent_themes: set[str]) -> QualityResult:
    errors: list[str] = []
    title = extract_title(card)
    tag_line = extract_tag_line(card)

    if not title:
        errors.append("缺少标题")
    if title in recent_titles:
        errors.append("标题最近 30 天内已出现")
    if not tag_line:
        errors.append("缺少 #每日认知 标签")
    missing_sections = [section for section in REQUIRED_SECTIONS if section not in card]
    if missing_sections:
        errors.append(f"缺少章节: {', '.join(missing_sections)}")

    if "今日一问" in card and "？" not in card and "?" not in card:
        errors.append("今日一问必须包含问题")

    if "10 分钟" not in card and "十分钟" not in card:
        errors.append("微行动需要明确 10 分钟左右可完成")

    if len(card) < 450:
        errors.append("内容过短，不足以支撑 3-5 分钟阅读")
    if len(card) > 2600:
        errors.append("内容过长，超过 3-5 分钟阅读范围")

    return QualityResult(ok=not errors, errors=errors)
```

- [ ] **Step 4: 运行测试确认通过**

Run:

```powershell
python -m unittest tests.test_quality -v
```

Expected: PASS。

## Task 5: OpenAI 内容生成

**Files:**
- Create: `cognitive_push/generator.py`

- [ ] **Step 1: 实现生成模块**

Create `cognitive_push/generator.py`:

```python
from __future__ import annotations

import json
import urllib.request

from cognitive_push.config import Config
from cognitive_push.themes import Theme


def build_prompt(theme: Theme, recent_titles: set[str]) -> str:
    recent = "\n".join(f"- {title}" for title in sorted(recent_titles)) or "- 无"
    return f"""请用中文生成一篇 3-5 分钟可读完的每日认知训练卡片。

当天主题：{theme.name}
主题说明：{theme.description}
可用认知模型参考：{", ".join(theme.examples)}

最近 30 天标题，不能重复：
{recent}

必须严格使用以下结构：

#每日认知/主题标签

标题：具体、有冲突感

1. 案例
2. 关键转折
3. 认知模型
4. 常见误判
5. 迁移到你
6. 今日一问
7. 微行动

要求：
- 内容要具体，避免鸡汤。
- 只讲一个主要认知模型。
- 今日一问必须能让读者联系自己的现实处境。
- 微行动必须是 10 分钟内可完成的小动作。
- 不要编造具体数据；如果使用公司或历史案例，只讲通用事实和决策逻辑。
"""


def generate_card(config: Config, theme: Theme, recent_titles: set[str]) -> str:
    payload = {
        "model": config.openai_model,
        "input": build_prompt(theme, recent_titles),
    }
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {config.openai_api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=90) as response:
        data = json.loads(response.read().decode("utf-8"))

    output_text = data.get("output_text", "").strip()
    if not output_text:
        raise RuntimeError("OpenAI response did not include output_text")
    return output_text
```

- [ ] **Step 2: 手动验证 prompt**

Run:

```powershell
python -c "from datetime import date; from cognitive_push.themes import theme_for_date; from cognitive_push.generator import build_prompt; print(build_prompt(theme_for_date(date(2026,6,1)), {'旧标题'}))"
```

Expected: 输出中文 prompt，包含“当天主题：决策偏误”和“旧标题”。

## Task 6: 企业微信和 flomo 发送

**Files:**
- Create: `cognitive_push/delivery.py`

- [ ] **Step 1: 实现 HTTP 发送模块**

Create `cognitive_push/delivery.py`:

```python
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


def send_wecom(webhook_url: str, content: str) -> None:
    payload = {
        "msgtype": "markdown",
        "markdown": {"content": content},
    }
    result = _post_json(webhook_url, payload)
    if result.get("errcode", 0) != 0:
        raise RuntimeError(f"WeCom send failed: {result}")


def send_flomo(webhook_url: str, content: str) -> None:
    payload = {"content": content}
    _post_json(webhook_url, payload)
```

- [ ] **Step 2: 手动验证模块可导入**

Run:

```powershell
python -c "from cognitive_push.delivery import send_wecom, send_flomo; print('delivery import ok')"
```

Expected: 输出 `delivery import ok`。

## Task 7: 主流程编排和重试

**Files:**
- Create: `cognitive_push/main.py`

- [ ] **Step 1: 实现主流程**

Create `cognitive_push/main.py`:

```python
from __future__ import annotations

from datetime import date
from time import sleep

from cognitive_push.config import load_config
from cognitive_push.delivery import send_flomo, send_wecom
from cognitive_push.generator import generate_card
from cognitive_push.quality import extract_tag_line, extract_title, validate_card
from cognitive_push.state import DailyRecord, StateStore
from cognitive_push.themes import theme_for_date


def _retry(action, attempts: int = 3, delay_seconds: int = 3) -> bool:
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


def run_once(today: date | None = None) -> None:
    config = load_config()
    current_day = today or date.today()
    theme = theme_for_date(current_day)
    store = StateStore(config.state_path)

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
            wecom_sent=wecom_sent,
            flomo_sent=flomo_sent,
        )
    )

    if not wecom_sent and not flomo_sent:
        raise RuntimeError("企业微信和 flomo 均发送失败，内容已记录到本地状态")


if __name__ == "__main__":
    run_once()
```

- [ ] **Step 2: 验证入口可加载**

Run:

```powershell
python -m cognitive_push.main
```

Expected: 如果未设置环境变量，输出缺少环境变量错误；设置真实环境变量后会执行一次完整推送。

## Task 8: README 和定时任务说明

**Files:**
- Create: `README.md`

- [ ] **Step 1: 写使用说明**

Create `README.md`:

```markdown
# 每日认知微信 + flomo 推送系统

这个项目每天生成一篇 3-5 分钟的认知案例卡片，推送到企业微信机器人，并同步保存到 flomo。

## 配置

复制 `.env.example` 中的变量名，在系统环境变量中配置真实值：

```text
OPENAI_API_KEY=你的 OpenAI API Key
OPENAI_MODEL=gpt-5
WECOM_WEBHOOK_URL=企业微信机器人 webhook
FLOMO_WEBHOOK_URL=flomo webhook
COGNITIVE_PUSH_STATE=data/state.json
COGNITIVE_PUSH_SEND_HOUR=8
```

## 手动运行

```powershell
python -m cognitive_push.main
```

## Windows 每天 08:00 定时运行

在任务计划程序中创建基本任务：

```text
触发器：每天 08:00
操作：启动程序
程序：python
参数：-m cognitive_push.main
起始于：项目所在目录
```

## 内容规则

每条内容包含：案例、关键转折、认知模型、常见误判、迁移到你、今日一问、微行动。
```

- [ ] **Step 2: 检查 README 可读性**

Run:

```powershell
Get-Content README.md
```

Expected: 能看到中文说明、环境变量和 Windows 任务计划程序配置。

## Task 9: 全量验证

**Files:**
- Modify: none

- [ ] **Step 1: 运行全部测试**

Run:

```powershell
python -m unittest discover -v
```

Expected: 所有测试 PASS。

- [ ] **Step 2: 验证无真实密钥写入仓库**

Run:

```powershell
Get-ChildItem -Recurse -File | Select-String -Pattern 'sk-[A-Za-z0-9_-]{20,}'
```

Expected: 不出现真实 OpenAI Key。

- [ ] **Step 3: 用真实环境变量做一次手动发送**

Run:

```powershell
python -m cognitive_push.main
```

Expected: 企业微信收到一篇认知卡片，flomo 中出现同一条内容，`data/state.json` 记录当天标题、主题标签和发送状态。

- [ ] **Step 4: 提交变更**

Run:

```powershell
git add cognitive_push tests README.md .env.example docs/superpowers/specs/2026-05-30-daily-cognitive-wechat-flomo-design-zh.md docs/superpowers/plans/2026-05-30-daily-cognitive-wechat-flomo.md
git commit -m "feat: add daily cognitive push automation"
```

Expected: 创建一个提交。如果当前机器没有安装 Git，则跳过提交，并在交付说明里列出所有新增和修改文件。

## 自检结果

- 设计要求已覆盖：企业微信机器人、08:00、通用知识生成、flomo webhook、30 天标题去重、失败重试、周日复盘主题。
- 没有保留待补充占位符。
- 类型和函数名在任务之间保持一致：`Config`、`Theme`、`StateStore`、`DailyRecord`、`validate_card`、`generate_card`、`send_wecom`、`send_flomo`、`run_once`。
