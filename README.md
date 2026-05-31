# 每日认知卡片

这个项目包含：

- Python 后端：生成每日认知判断力卡片，提供 iOS App API，并通过 APNs 推送到手机。
- SwiftUI iOS 源码骨架：今日卡片、回答保存、微行动、历史和周复盘。

## 后端配置

参考 `.env.example` 设置环境变量：

```text
DEEPSEEK_API_KEY=你的 DeepSeek API Key
DEEPSEEK_MODEL=deepseek-chat
COGNITIVE_PUSH_DATABASE=data/app.sqlite3
COGNITIVE_PUSH_API_HOST=127.0.0.1
COGNITIVE_PUSH_API_PORT=8080
APNS_TEAM_ID=你的 Apple Team ID
APNS_KEY_ID=你的 APNs Key ID
APNS_BUNDLE_ID=com.example.dailycognition
APNS_PRIVATE_KEY_PATH=secrets/AuthKey_你的KeyID.p8
APNS_AUTH_TOKEN=
APNS_ENVIRONMENT=sandbox
```

推荐配置 `APNS_PRIVATE_KEY_PATH`，后端会用 `.p8` 私钥生成 APNs provider token。部署环境需要安装 Python `cryptography` 包。`APNS_AUTH_TOKEN` 只适合临时调试时手动传入已生成的 provider token。

pushplus 和 flomo 仍可作为每日提醒与归档通道：

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

## iOS App

SwiftUI 源码位于：

```text
ios/DailyCognitionApp/Sources/DailyCognitionApp
```

在 Xcode 中新建 iOS App 工程后，把这些 Swift 文件加入 app target，并在 `AppConfig.swift` 中设置后端 API 地址。

真机推送需要：

- Apple Developer 账号。
- App target 开启 Push Notifications capability。
- Bundle ID 与 `APNS_BUNDLE_ID` 一致。
- 后端可访问 Apple APNs 服务。

## 测试

```powershell
python -m unittest discover -v
```

## GitHub Actions 免费定时运行

项目已经包含 `.github/workflows/daily-cognitive.yml`。上传到 GitHub 后，它会在每天北京时间 08:00 自动运行，也可以在 GitHub App 或网页里手动点 Run workflow。

在仓库的 Settings -> Secrets and variables -> Actions 里添加这些 Secrets：

```text
DEEPSEEK_API_KEY
DEEPSEEK_MODEL
PUSHPLUS_TOKEN
FLOMO_WEBHOOK_URL
```

推荐值：

```text
DEEPSEEK_MODEL=deepseek-chat
```
