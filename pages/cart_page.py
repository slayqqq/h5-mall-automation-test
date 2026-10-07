# -*- coding: utf-8 -*-
"""
购物车页对象（SauceDemo）
对应你商城里的：购物车页（数量增减 / 单选全选 / 删除 / 金额刷新）
"""
from selenium.webdriver.common.by import By

from keywords import click, assert_text


class CartPage:
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")   # 购物车中的商品名
    CHECKOUT_BTN = (By.ID, "checkout")                   # 去结算
    CONTINUE_BTN = (By.ID, "continue-shopping")          # 继续购物

    def __init__(self, driver):
        self.driver = driver

    def assert_item_in_cart(self, item_name="Sauce Labs Backpack"):
        """断言商品已在购物车中"""
        assert_text(self.driver, *self.ITEM_NAME, item_name)
        return self

    def goto_checkout(self):
        """进入结算页"""
        click(self.driver, *self.CHECKOUT_BTN)
        return self
