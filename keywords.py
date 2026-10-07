# -*- coding: utf-8 -*-
"""
关键字库：对 Selenium 常用操作做二次封装。
每个操作统一了"显式等待 + 日志 + 可读性"，页面对象（pages/）只调用这里的函数，
不直接写 driver.find_element —— 这就是"关键字"思想在项目一里的体现。
"""
import os
import time
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger("keywords")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


def open_url(driver, url):
    """打开页面"""
    logger.info("打开页面: %s", url)
    driver.get(url)
    return driver


def wait_element(driver, by, value, timeout=15):
    """显式等待元素可见，超时抛异常（比隐式等待更可控，是面试考点）"""
    logger.info("等待元素可见: %s=%s", by, value)
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, value))
    )


def input_text(driver, by, value, text):
    """输入文本：先清空再输入，避免残留值"""
    el = wait_element(driver, by, value)
    el.clear()
    el.send_keys(text)
    logger.info("输入文本: %s=%s <- %s", by, value, text)
    return el


def click(driver, by, value):
    """点击元素（等待可点击状态）"""
    el = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((by, value)))
    el.click()
    logger.info("点击: %s=%s", by, value)
    return el


def get_text(driver, by, value):
    """获取元素文本"""
    return wait_element(driver, by, value).text


def assert_text(driver, by, value, expected):
    """断言元素文本包含预期内容，失败即用例失败"""
    el = wait_element(driver, by, value)
    actual = el.text
    assert expected in actual, f"断言失败: 期望包含[{expected}], 实际为[{actual}]"
    logger.info("断言通过: %s=%s 包含 [%s]", by, value, expected)
    return actual


def screenshot(driver, name):
    """保存截图（失败证据）"""
    os.makedirs("screenshots", exist_ok=True)
    path = f"screenshots/{name}_{int(time.time())}.png"
    driver.save_screenshot(path)
    logger.info("截图保存: %s", path)
    return path


def switch_frame(driver, frame_ref):
    """切换到 iframe（H5 页面常见，切错了元素找不到）"""
    driver.switch_to.frame(frame_ref)


def switch_to_default(driver):
    """切回主文档"""
    driver.switch_to.default_content()
