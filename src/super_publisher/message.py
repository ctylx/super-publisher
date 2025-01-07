import time
import hmac
import hashlib
import base64
import urllib.parse
import requests

secret = "SEC87f310fde7721b7eb4008b6de08236e3eccc30f9cff33f625d93a3d0957c24a8"
apiurl = "https://oapi.dingtalk.com/robot/send?access_token=0285f1dc04614dd34622e299ddafd3a19852d57c8285d25e13f3325f84609d20"


def calculate_sign(timestamp: str):
    secret_enc = secret.encode("utf-8")
    string_to_sign_enc = f"{timestamp}\n{secret}".encode("utf-8")
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256)
    return urllib.parse.quote_plus(base64.b64encode(hmac_code.digest()))


def send_notify(content: str):
    timestamp = str(round(time.time() * 1000))
    sign = calculate_sign(timestamp)
    url = f"{apiurl}&timestamp={timestamp}&sign={sign}"
    message = {"msgtype": "text", "text": {"content": content}}
    return requests.post(url=url, json=message)


if __name__ == "__main__":
    response = send_notify("这是一条测试消息")
    print(response.text)
