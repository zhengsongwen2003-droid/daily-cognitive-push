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
