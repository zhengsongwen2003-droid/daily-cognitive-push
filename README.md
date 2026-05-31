# 每日认知卡片

这个项目现在包含两部分：

- Python 后端：每天生成认知判断力训练卡片，提供 iOS App API，并可通过 APNs 推送到手机。
- SwiftUI iOS 源码骨架：展示今日卡片、保存回答和微行动、查看历史与周复盘。

## 后端配置

参考 `.env.example` 设置环境变量：

```text
OPENAI_API_KEY=你的 OpenAI API Key
OPENAI_MODEL=gpt-5
COGNITIVE_PUSH_DATABASE=data/app.sqlite3
COGNITIVE_PUSH_API_HOST=127.0.0.1
COGNITIVE_PUSH_API_PORT=8080
APNS_TEAM_ID=你的 Apple Team ID
APNS_KEY_ID=你的 APNs Key ID
APNS_BUNDLE_ID=com.example.dailycognition
APNS_AUTH_TOKEN=你的 APNs provider token
APNS_ENVIRONMENT=sandbox
```

pushplus 和 flomo 可以作为每日微信提醒与知识归档通道：

```text
PUSHPLUS_TOKEN=pushplus token
FLOMO_WEBHOOK_URL=flomo webhook
COGNITIVE_PUSH_STATE=data/state.json
COGNITIVE_PUSH_SEND_HOUR=8
```

## 运行后端 API

```powershell
python -m cognitive_push.main --serve-api
```

API:

- `POST /devices` 注册 iOS APNs device token。
- `GET /cards/today` 获取今日卡片。
- `POST /cards/{card_id}/reflection` 保存今日回答和微行动状态。
- `GET /cards/history` 获取历史卡片。
- `GET /reviews/current-week` 获取本周复盘。

## 发送 iOS 推送

```powershell
python -m cognitive_push.main --send-ios-notification
```

这个命令会生成或复用当天卡片，然后向已注册设备发送 APNs 通知。

## 旧通道手动运行

```powershell
python -m cognitive_push.main --force
```

这个入口会把每日卡片发送到 pushplus，并同步保存到 flomo。

## iOS App

SwiftUI 源码位于：

```text
ios/DailyCognitionApp/Sources/DailyCognitionApp
```

在 Xcode 中新建 iOS App 工程后，把这些 Swift 文件加入 app target，并在 `AppConfig.swift` 中设置后端 API 地址。

## 测试

```powershell
python -m unittest discover -v
```
