# -*- coding: utf-8 -*-
"""
电科商城 H5 接口自动化（模板）
================================================
被测接口特征：
  - 统一网关：POST https://app.cetconline.com/veopen/webapi
  - 通过 header `service` 区分业务（WEBAPI_FLSC_getCartList 等）
  - 请求体 hex 加密（黑盒无法构造新参数，只能重放原始 body）
  - header 带 sign 签名，重放过期后回浏览器重抓一次即可

注意：真实 token / sign / cookie 不要写在本文件里，
      请从环境变量或本地 config.py（已 gitignore）读取。
"""
import os
import requests
import pytest

BASE = "https://app.cetconline.com/veopen/webapi"

# 从环境变量读敏感信息（避免硬编码泄露）
AUTH_TOKEN = os.getenv("CETCONLINE_TOKEN", "<your_token_here>")
AUTH_COOKIE = os.getenv("CETCONLINE_COOKIE", "https_waf_cookie=...; cna=...")

# 公共头（不含 sign，每个接口单独带）
COMMON_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Apphost": "app.cetconline.com",
    "Content-Type": "text/plain",
    "Origin": "https://app.cetconline.com",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) "
                  "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1",
    "channelId": "QDH",
    "deviceType": "1",
    "systemId": "VETECH",
    "timeout": "60000",
    "token": AUTH_TOKEN,
    "Cookie": AUTH_COOKIE,
}


def _post(service: str, referer: str, sign: str, body: str):
    """统一请求封装：每个接口从浏览器重抓 cURL 后填这 4 个参数"""
    headers = dict(COMMON_HEADERS)
    headers.update({
        "service": service,
        "Referer": referer,
        "sign": sign,
        "operateTime": "2026-01-01 00:00:00",  # 重抓时更新
    })
    return requests.post(f"{BASE}?{service}", headers=headers, data=body, timeout=10)


class TestReadOnlyAPIs:
    """只读接口重放测试（每个接口 3 条断言）"""

    def test_cart_list_status_200(self):
        # TODO: 抓到新的 cURL 后填入 service/referer/sign/body
        pytest.skip("需要从浏览器重抓新鲜 cURL 后填入，避免 token 过期")
        # r = _post("WEBAPI_FLSC_getCartList", "/mallapp/welfareMallTabs/shopping", "<sign>", "<hex_body>")
        # assert r.status_code == 200

    def test_goods_detail_response_time(self):
        pytest.skip("同上，需要新鲜 sign")

    def test_order_list_business_code(self):
        pytest.skip("同上，需要新鲜 sign")
