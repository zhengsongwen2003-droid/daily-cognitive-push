# 每日认知卡片网页版

这是一个静态网页小应用，可以直接打开 `index.html` 使用。

手机访问推荐发布到 GitHub Pages。仓库已经包含 `.github/workflows/pages.yml`，推送到 `main` 后会把 `web/` 目录部署成可公开访问的网页。

功能：

- 查看每日认知训练卡片
- 切换不同主题卡片
- 保存今日回答到浏览器本地
- 标记 10 分钟微行动完成
- 查看复盘和历史记录

本地数据保存在浏览器的 `localStorage`，不会上传到服务器。

同一 Wi-Fi 下手机访问：

```powershell
powershell -ExecutionPolicy Bypass -File .\start-phone-server.ps1
```

脚本会显示手机可打开的局域网地址。
