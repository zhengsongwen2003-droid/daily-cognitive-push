# 每日认知微信 + flomo 推送系统

这个项目每天生成一篇 3-5 分钟的认知案例卡片，推送到企业微信机器人，并同步保存到 flomo。

## 配置

参考 `.env.example` 中的变量名，在系统环境变量中配置真实值：

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

这个命令会检查当前小时是否等于 `COGNITIVE_PUSH_SEND_HOUR`。如果想立刻试发一次，可以使用：

```powershell
python -m cognitive_push.main --force
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

系统会保存最近 30 天记录，避免重复标题。企业微信或 flomo 发送失败时会重试，两个入口都失败时会保留本地记录，避免当天内容丢失。

## 测试

本项目使用 Python 标准库 `unittest`，不需要额外安装测试框架：

```powershell
python -m unittest discover -v
```
