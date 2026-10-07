# -*- coding: utf-8 -*-
"""
结算页对象（SauceDemo）：重点演示"金额计算校验"
对应你商城里的：结算页（商品合计 + 运费/优惠 + 应付总额）
"""
import re

from selenium.webdriver.common.by import By

from keywords import input_text, click, wait_element, assert_text


class CheckoutPage:
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BTN = (By.ID, "continue")
    ITEM_TOTAL = (By.CLASS_NAME, "summary_subtotal_label")  # 商品合计
    TAX = (By.CLASS_NAME, "summary_tax_label")              # 税费
    TOTAL = (By.CLASS_NAME, "summary_total_label")          # 应付总额
    FINISH_BTN = (By.ID, "finish")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")    # 下单成功提示

    def __init__(self, driver):
        self.driver = driver

    def fill_info(self, first, last, postal):
        """填写收货信息并进入金额确认页"""
        input_text(self.driver, *self.FIRST_NAME, first)
        input_text(self.driver, *self.LAST_NAME, last)
        input_text(self.driver, *self.POSTAL_CODE, postal)
        click(self.driver, *self.CONTINUE_BTN)
        return self

    def assert_amount(self):
        """
        金额校验（面试高频考点）：
        应付总额 = 商品合计 + 税费，页面展示的金额必须满足该口径。
        金额解析从文本 "$29.99" 中取 29.99。
        """
        item_total = self._parse_money(wait_element(self.driver, *self.ITEM_TOTAL).text)
        tax = self._parse_money(wait_element(self.driver, *self.TAX).text)
        total = self._parse_money(wait_element(self.driver, *self.TOTAL).text)
        assert abs((item_total + tax) - total) < 0.01, \
            f"金额校验失败: 商品合计{item_total} + 税费{tax} != 应付总额{total}"
        print(f"金额校验通过: 商品合计{item_total} + 税费{tax} = 应付总额{total}")
        return self

    def finish_order(self):
        """完成下单"""
        click(self.driver, *self.FINISH_BTN)
        assert_text(self.driver, *self.COMPLETE_HEADER, "Thank you for your order!")
        return self

    @staticmethod
    def _parse_money(text):
        """从 '$29.99' 提取 29.99；解析失败按 0 处理并打印警告"""
        match = re.search(r"\$([\d.]+)", text)
        if not match:
            print(f"警告: 无法解析金额文本 [{text}]")
            return 0.0
        return float(match.group(1))
