# -*- coding: utf-8 -*-
"""
P0 核心交易链路自动化用例：
  登录 → 加购 → 购物车校验 → 结算 → 金额校验 → 完成下单
对应你商城的手工用例 H5_ORDER_001（docs/测试用例模板.csv）
"""
from config import BASE_URL, USERNAME, PASSWORD
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


class TestShoppingFlow:

    def test_full_purchase_flow(self, driver):
        """P0-完整购买链路 + 金额计算校验（面试展示这条最加分）"""
        # 1. 登录
        driver.get(BASE_URL)
        LoginPage(driver).login(USERNAME, PASSWORD).login_success()

        # 2. 首页加购第一件商品，断言角标
        home = HomePage(driver)
        home.add_first_item()
        home.assert_cart_badge("1")

        # 3. 进入购物车，断言商品在车
        home.goto_cart()
        CartPage(driver).assert_item_in_cart().goto_checkout()

        # 4. 结算：填写收货信息，校验金额（商品合计 + 税费 = 应付总额）
        CheckoutPage(driver).fill_info("Tom", "Li", "10001").assert_amount().finish_order()
