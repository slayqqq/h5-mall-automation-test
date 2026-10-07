# -*- coding: utf-8 -*-
"""
商品列表页对象（SauceDemo）
对应你商城里的：首页 → 商品搜索/分类列表页
"""
from selenium.webdriver.common.by import By

from keywords import click, assert_text


class HomePage:
    TITLE = (By.CLASS_NAME, "title")
    ADD_TO_CART = (By.ID, "add-to-cart-sauce-labs-backpack")  # 第一个商品"加购"按钮
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")          # 右上角购物车入口
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")        # 购物车角标数字

    def __init__(self, driver):
        self.driver = driver

    def add_first_item(self):
        """把第一个商品加入购物车"""
        click(self.driver, *self.ADD_TO_CART)
        return self

    def assert_cart_badge(self, expected_number):
        """断言购物车角标数字"""
        assert_text(self.driver, *self.CART_BADGE, expected_number)
        return self

    def goto_cart(self):
        """进入购物车"""
        click(self.driver, *self.CART_ICON)
        return self
