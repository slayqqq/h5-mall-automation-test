# -*- coding: utf-8 -*-
"""
登录页对象（Page Object）
默认针对 SauceDemo（公开演示商城）编写，下载即可运行验证框架。

== 如何适配到你的"电科商城" ==
你的登录页（见截图）：验证码登录 / 密码登录 双 Tab，页面包含：
  手机号输入框、图形验证码输入框、短信验证码输入框、获取验证码按钮、服务协议勾选、注册/登录按钮
适配步骤：
  1. 浏览器打开商城登录页，按 F12 → Elements，找到每个元素的 id / class / xpath
  2. 把下方【电科商城版定位】注释里的表达式，按 F12 看到的真实值补全
  3. 短信验证码自动化需配合"万能验证码 / Cookie 绕过 / 手动输入"，见 README 第 4 节
"""
from selenium.webdriver.common.by import By

from keywords import input_text, click, assert_text


class LoginPage:
    # ===== 元素定位（SauceDemo 版，可直接运行）=====
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    ERROR_MSG = (By.XPATH, "//h3[@data-test='error']")
    TITLE = (By.CLASS_NAME, "title")

    # ===== 电科商城版定位（示例占位，需按 F12 检查后替换）=====
    # MALL_PHONE = (By.XPATH, "//input[@placeholder='请输入手机号']")
    # MALL_GRAPHIC_CODE = (By.XPATH, "//input[@placeholder='请输入图形验证码']")
    # MALL_GET_SMS_BTN = (By.XPATH, "//button[contains(text(),'获取验证码')]")
    # MALL_SMS_CODE = (By.XPATH, "//input[@placeholder='请输入短信验证码']")
    # MALL_AGREE = (By.XPATH, "//span[contains(text(),'同意')]")
    # MALL_LOGIN_BTN = (By.XPATH, "//button[contains(text(),'注册/登录')]")

    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        """SauceDemo：账号密码登录"""
        input_text(self.driver, *self.USERNAME, username)
        input_text(self.driver, *self.PASSWORD, password)
        click(self.driver, *self.LOGIN_BTN)
        return self

    def login_success(self):
        """断言登录成功：进入商品页"""
        assert_text(self.driver, *self.TITLE, "Products")
        return self

    def login_fail(self, expected_error):
        """断言登录失败：出现错误提示"""
        assert_text(self.driver, *self.ERROR_MSG, expected_error)
        return self
