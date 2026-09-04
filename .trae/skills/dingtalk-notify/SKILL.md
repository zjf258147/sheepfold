---
name: "dingtalk-notify"
description: "Send DingTalk (钉钉) group notifications via webhook with HMAC-SHA256 signing. Invoke when user needs to add DingTalk robot notifications to any project."
---

# DingTalk Notify (钉钉群机器人通知)

A reusable, zero-dependency DingTalk group robot notification module. Supports text and markdown messages with HMAC-SHA256 signing.

## Quick Start

```python
from dingtalk import DingTalkNotifier

# 1. Create notifier
bot = DingTalkNotifier(
    webhook="https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN",
    secret="SEC_YOUR_SECRET"
)

# 2. Send text message
bot.send_text("升级完成 ✅")

# 3. Send markdown message
bot.send_markdown(
    title="升级通知",
    text="## 升级结果\n- 设备: HD001\n- 状态: **成功** ✅"
)
```

## API Reference

### `DingTalkNotifier(webhook, secret, enabled=True)`

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `webhook` | `str` | required | DingTalk robot webhook URL |
| `secret` | `str` | required | HMAC-SHA256 signing secret |
| `enabled` | `bool` | `True` | Global on/off switch |

### `send_text(message: str) -> bool`

Send plain text message. Returns `True` on success, `False` on failure (never raises).

### `send_markdown(title: str, text: str) -> bool`

Send markdown message with title. Returns `True` on success, `False` on failure (never raises).

## Design Principles

| Principle | Implementation |
|-----------|---------------|
| **Never Block** | All exceptions caught internally, `send_*` always returns `bool` |
| **Zero Config** | Constructor takes all params, no config file dependency |
| **Single File** | Copy `dingtalk.py` into any project, `import` and use |
| **Type Safe** | Full type hints for IDE autocompletion |

## Files to Copy

Just copy this single file to your project:

```
dingtalk.py    ← The only file you need
```

## Dependencies

Only Python standard library:
- `hashlib` — HMAC-SHA256 signing
- `hmac` — HMAC computation
- `base64` — Base64 encoding
- `urllib.parse` — URL encoding
- `time` — Timestamp generation

Optional (for HTTP requests):
- `requests` — If not available, falls back to `urllib.request`

## Advanced: @Someone / @All

```python
bot.send_text("升级失败 ⚠️", at_mobiles=["13800138000"], at_all=False)
bot.send_text("紧急通知 🚨", at_all=True)
```

## Advanced: Custom Timeout

```python
bot = DingTalkNotifier(webhook, secret, timeout=10)
bot.send_text("Large notification...")
```