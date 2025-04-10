# -*- coding:utf-8 -*-

import datetime
import requests
import time
import hmac
import hashlib
import base64
import urllib.parse


class DingTalkBot:
    def __init__(self, webhook_url, secret):
        self.webhook_url = webhook_url
        self.secret = secret

    def _generate_signature(self):
        """
        生成签名，用于加签验证
        :return: 包含时间戳和签名的字典
        """
        if not self.secret:
            return {}

        timestamp = str(round(time.time() * 1000))
        string_to_sign = f"{timestamp}\n{self.secret}"
        hmac_code = hmac.new(
            self.secret.encode("utf-8"),
            string_to_sign.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return {"timestamp": timestamp, "sign": sign}

    def send_message(self, msg_type, content, **kwargs):
        """
        发送消息
        :param msg_type: 消息类型 (text, markdown, link, actionCard, feedCard)
        :param content: 消息内容（根据类型不同而变化）
        :param kwargs: 其他可选参数（标题、链接等）
        :return: 钉钉响应结果
        """
        # 生成完整的 URL（如果使用加签）
        signature = self._generate_signature()
        if signature:
            url = f"{self.webhook_url}&timestamp={signature['timestamp']}&sign={signature['sign']}"
        else:
            url = self.webhook_url

        # 构建消息数据
        data = {"msgtype": msg_type}

        if msg_type == "text":
            data["text"] = {"content": content}

        elif msg_type == "markdown":
            data["markdown"] = {"title": kwargs.get("title", "Markdown Message"), "text": content}

        elif msg_type == "link":
            data["link"] = {
                "title": kwargs.get("title", "Link Message"),
                "text": content,
                "messageUrl": kwargs.get("message_url", ""),
                "picUrl": kwargs.get("pic_url", ""),
            }

        elif msg_type == "actionCard":
            data["actionCard"] = {
                "title": kwargs.get("title", "Action Card"),
                "text": content,
                "btnOrientation": kwargs.get("btn_orientation", "0"),
                "btns": kwargs.get("btns", []),
            }

        elif msg_type == "feedCard":
            data["feedCard"] = {"links": kwargs.get("links", [])}

        else:
            raise ValueError("Unsupported msg_type: {}".format(msg_type))

        # 发送请求
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=data, headers=headers)

        return response.json()

    def quick_detail_info(self, msg_type="markdown", **kwargs):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        service = kwargs.get("service", "定时任务")
        title = kwargs.get("title", "")
        content = kwargs.get("content", "")
        error_level = kwargs.get("error_level", 0)
        at_mobiles = kwargs.get("at_mobiles", [])
        if not title or not content:
            raise ValueError("Missing parameter, Please check parameter")
        data = {"msgtype": msg_type}
        data["markdown"] = {
            "title": title,
            "text": (
                    "#### **告警通知**\n\n🚨 "
                    f"**标题**：{title}\n\n"
                    f"**服务异常**：{service}\n\n"
                    f"> **告警等级**：P{error_level}\n\n"
                    f"- **发生时间**：{current_time}\n"
                    f"- **错误信息**：{content}\n\n"
                    + ''.join([f"@{mobile}" for mobile in at_mobiles])
            ),
        }
        data["at"] = {
            "atMobiles": at_mobiles,
            "isAtAll": False,
        }
        signature = self._generate_signature()
        url = f"{self.webhook_url}&timestamp={signature['timestamp']}&sign={signature['sign']}"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=data, headers=headers)
        return response.json()


if __name__ == "__main__":
    bot = DingTalkBot()

    # 发送告警消息
    # response_text = bot.send_message("text", "你好这是一条告警信息")
    # print("Text Message Response:", response_text)

    # title = "告警通知"
    # content = ("#### **告警通知**\n\n🚨 "
    #            "**服务异常**：服务A请求失败\n\n"
    #            "> **告警等级**：P0\n\n"
    #            "- **发生时间**：2024-11-15 12:30:00\n"
    #            "- **错误信息**：响应超时\n\n"
    #            "[点击查看详情](http://example.com)")
    # bot.send_message(msg_type="markdown", title=title, content=content)
    # response = bot.quick_detail_info(title="ces", content="ces",at_mobiles=["13733454523"])
    # print(response)
