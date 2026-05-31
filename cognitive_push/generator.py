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
- 微行动必须是 10 分钟内可完成的小动作，并且第 7 段正文必须出现字面量“10 分钟”。
- 不要编造具体数据；如果使用公司或历史案例，只讲通用事实和决策逻辑。
- 不要输出前言、说明、总结或额外 Markdown 分隔线。
- 章节标题可以加粗，但必须保留“1. 案例”到“7. 微行动”这 7 个标题。
"""


def generate_card(config: Config, theme: Theme, recent_titles: set[str]) -> str:
    payload = {
        "model": config.deepseek_model,
        "messages": [
            {
                "role": "user",
                "content": build_prompt(theme, recent_titles),
            }
        ],
        "stream": False,
    }
    request = urllib.request.Request(
        "https://api.deepseek.com/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {config.deepseek_api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=90) as response:
        data = json.loads(response.read().decode("utf-8"))

    choices = data.get("choices", [])
    output_text = ""
    if choices:
        output_text = choices[0].get("message", {}).get("content", "").strip()
    if not output_text:
        raise RuntimeError("DeepSeek response did not include message content")
    return output_text
