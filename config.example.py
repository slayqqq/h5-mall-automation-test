# -*- coding: utf-8 -*-
"""
配置模板：复制本文件为 config.py，再填入你自己的真实 cookie。
config.py 已在 .gitignore 中，不会被传到 GitHub。
"""

# ===== 被测系统 =====
BASE_URL = "https://app.cetconline.com"
HOMEPAGE_PATH = "/mallapp/welfareMallTabs/welfareTemplateHome"

# ===== Cookie 注入（绕开图形+短信验证码）=====
# 操作方法：
# 1. 电脑 Chrome 手动登录 https://app.cetconline.com
# 2. F12 → Application → Cookies → https://app.cetconline.com
# 3. 把所有 Name / Value 抄到下面列表
# 4. domain 可留空，conftest.py 会自动去掉，避免域名不匹配
COOKIES_TO_INJECT = [
    # 示例（请替换成你自己的 cookie）：
    # {"name": "your_cookie_name", "value": "your_cookie_value", "path": "/"},
]

# ===== 等待时间 =====
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 15

# ===== H5 手机模拟 =====
USE_MOBILE = True
MOBILE_EMULATION = {
    "deviceName": "iPhone 12 Pro",
}

# ===== 输出目录 =====
SCREENSHOT_DIR = "screenshots"
REPORT_DIR = "reports"
LOG_DIR = "logs"
