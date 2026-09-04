"""
dingtalk.py - 钉钉群机器人通知模块（零依赖，单文件可复用）

用法:
    from dingtalk import DingTalkNotifier

    bot = DingTalkNotifier(
        webhook="https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN",
        secret="SEC_YOUR_SECRET",
    )
    bot.send_text("升级完成 ✅")
    bot.send_markdown("升级通知", "## 结果\n- 设备: HD001\n- 状态: 成功")

依赖: 仅 Python 标准库 + requests（可选，无则回退到 urllib）
"""

import base64
import hashlib
import hmac
import json
import time
import urllib.parse
from typing import List, Optional

try:
    import requests
    _HAS_REQUESTS = True
except ImportError:
    import urllib.request
    _HAS_REQUESTS = False


class DingTalkNotifier:
    """钉钉群机器人通知器。

    Attributes:
        webhook: 机器人 Webhook URL
        secret: 加签密钥
        enabled: 全局开关，False 时不发送任何消息
        timeout: HTTP 请求超时（秒）
    """

    def __init__(self, webhook: str, secret: str, enabled: bool = True,
                 timeout: int = 5):
        self.webhook = webhook
        self.secret = secret
        self.enabled = enabled
        self.timeout = timeout

    # ====== 公共 API ======

    def send_text(self, message: str, at_mobiles: Optional[List[str]] = None,
                  at_all: bool = False) -> bool:
        """发送文本消息。

        Args:
            message: 消息内容
            at_mobiles: 要 @ 的手机号列表
            at_all: 是否 @所有人

        Returns:
            True 发送成功，False 发送失败（不抛异常）
        """
        at_data = {}
        if at_mobiles:
            at_data["atMobiles"] = at_mobiles
        if at_all:
            at_data["isAtAll"] = True

        data = {
            "msgtype": "text",
            "text": {"content": message},
        }
        if at_data:
            data["at"] = at_data

        return self._post(data)

    def send_markdown(self, title: str, text: str) -> bool:
        """发送 Markdown 消息。

        Args:
            title: 消息标题
            text: Markdown 内容

        Returns:
            True 发送成功，False 发送失败（不抛异常）
        """
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text,
            },
        }
        return self._post(data)

    # ====== 内部实现 ======

    def _build_url(self) -> str:
        """构建带签名的 Webhook URL。"""
        timestamp = str(round(time.time() * 1000))
        string_to_sign = f"{timestamp}\n{self.secret}"
        hmac_code = hmac.new(
            self.secret.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            digestmod=hashlib.sha256,
        ).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return f"{self.webhook}&timestamp={timestamp}&sign={sign}"

    def _post(self, data: dict) -> bool:
        """发送 HTTP POST 请求（内部方法，吞所有异常）。"""
        if not self.enabled:
            return False

        url = self._build_url()
        body = json.dumps(data).encode('utf-8')

        try:
            if _HAS_REQUESTS:
                resp = requests.post(url, data=body, timeout=self.timeout,
                                     headers={'Content-Type': 'application/json'})
                return resp.status_code == 200 and resp.json().get('errcode') == 0
            else:
                req = urllib.request.Request(url, data=body, method='POST',
                                             headers={'Content-Type': 'application/json'})
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    result = json.loads(resp.read().decode('utf-8'))
                    return result.get('errcode') == 0
        except Exception:
            return False


# ====== 自测 ======
if __name__ == "__main__":
    print("=== 钉钉通知模块自测 ===\n")
    print("请设置 WEBHOOK 和 SECRET 后运行:")
    print("  bot = DingTalkNotifier(WEBHOOK, SECRET)")
    print("  bot.send_text('测试消息 ✅')")