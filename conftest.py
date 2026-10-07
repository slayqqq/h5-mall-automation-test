# -*- coding: utf-8 -*-
"""
pytest 全局 fixture：
  1. driver：每个用例独立浏览器（H5 用 Chrome 手机模拟模式）
  2. 启动后自动注入 Cookie，跳过验证码
  3. 用例失败自动截图
"""
import os
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from config import (BASE_URL, COOKIES_TO_INJECT, HOMEPAGE_PATH,
                    IMPLICIT_WAIT, MOBILE_EMULATION, USE_MOBILE,
                    SCREENSHOT_DIR)


def _create_driver():
    options = Options()
    if USE_MOBILE:
        options.add_experimental_option("mobileEmulation", MOBILE_EMULATION)
    else:
        options.add_argument("--window-size=1280,800")
    # options.add_argument("--headless=new")

    # 用项目目录下的 chromedriver.exe（国内下载不了 Selenium 自动驱动，手动放）
    driver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver.exe")
    if os.path.exists(driver_path):
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(IMPLICIT_WAIT)
    return driver


def _inject_cookies(drv):
    """
    Cookie 注入三步走：
      1. 先访问目标域名
      2. 清空旧 cookie
      3. 逐个 add_cookie（自动去掉 domain 字段，避免域名不匹配报错）
      4. 刷新页面
    """
    if not COOKIES_TO_INJECT:
        print("[警告] config.py 里 COOKIES_TO_INJECT 是空的，没注入 cookie")
        return

    drv.get(BASE_URL)
    time.sleep(2)  # 等首屏加载
    drv.delete_all_cookies()
    for ck in COOKIES_TO_INJECT:
        # 去掉 domain 和 expiry，让 Selenium 自动按当前页面域名设置
        ck_to_set = {k: v for k, v in ck.items() if k not in ("domain", "expiry", "sameSite")}
        try:
            drv.add_cookie(ck_to_set)
        except Exception as e:
            print(f"[警告] cookie {ck.get('name')} 注入失败: {e}")
    drv.get(BASE_URL + HOMEPAGE_PATH)
    time.sleep(6)  # 等 5 秒广告 / 开屏页过去


@pytest.fixture(scope="function")
def driver():
    drv = _create_driver()
    _inject_cookies(drv)
    yield drv
    drv.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        drv = item.funcargs.get("driver")
        if drv:
            os.makedirs(SCREENSHOT_DIR, exist_ok=True)
            path = os.path.join(SCREENSHOT_DIR, f"{item.name}_失败.png")
            try:
                drv.save_screenshot(path)
                print(f"失败截图已保存: {path}")
            except Exception as e:
                print(f"截图失败: {e}")
