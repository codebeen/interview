#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from datetime import datetime

from constans import GOODS_TYPE_MAP


class Classify(object):
    def __init__(self, goods):
        self.goods = goods

    def get_good_iter(self, is_evert=False):
        goods_msg_list = self.goods.strip().split("\n")
        if is_evert:
            goods_msg_list = goods_msg_list[::-1]
        for goods_msg in goods_msg_list:
            yield goods_msg.strip()

    def get_discounts(self):
        discount_package = {}
        goods_iter = self.get_good_iter()
        for goods_msg in goods_iter:
            if goods_msg.count("|") != 2:

                # there is no discount message.
                break

            discount_item = goods_msg.split("|")
            expire_string = discount_item[0].strip()
            bill_date = self.get_bill_date()
            if bill_date != expire_string:

                # sorry! the discount information has expired.
                break
            # expire_date = datetime.strptime(expire_string, "%Y.%m.%d")
            # today = datetime.now()
            # if not (expire_date - today).total_seconds():
            #
            #     # sorry! the discount information has expired.
            #     break
            goods_type = discount_item[2].strip()
            discount_value = discount_item[1].strip()

            # every type of discounts just use one pice on a time
            discount_package[goods_type] = discount_value
        return discount_package

    def get_goods(self):
        """get goods mess from string messages"""

        goods_list = []
        goods_iter = self.get_good_iter()
        goods_re_str = r"\d+\s+\*\s+\w+\s+:\s+\d+\.\d{2}"
        for goods_msg in goods_iter:
            goods_msg = goods_msg.strip()
            if not re.search(goods_re_str, goods_msg):
                continue

            goods_msg_list = goods_msg.split("*")
            goods_counts = int(goods_msg_list[0].strip())
            price_lsit = goods_msg_list[1].split(":")
            goods_name = price_lsit[0].strip()

            #TODO check goods is legitimate or not
            goods_price = float(price_lsit[1].strip())

            goods_package = {"goods_name": goods_name,
             "total_price": float(goods_counts * goods_price)}
            goods_list.append(goods_package)
        return goods_list

    def get_coupon(self):
        goods_iter = self.get_good_iter(is_evert=True)
        coupon_re_str = r"\d+\.\d{1,2}\.\d{1,2}\s+\d+\s+\d+"
        for goods_msg in goods_iter:
            goods_msg = goods_msg.strip()
            if re.match(coupon_re_str, goods_msg):
                goods_msg = goods_msg.split()
                expire_date = datetime.strptime(goods_msg[0], "%Y.%m.%d")
                today = datetime.now()
                if (expire_date - today).total_seconds() < 0:

                    # sorry! the discount information has expired.
                    break
                return {"condition": float(goods_msg[2]),
                        "remit": float(goods_msg[1])}

    def get_bill_date(self):
        bill_date_str = ""
        goods_iter = self.get_good_iter(is_evert=True)
        date_re_str = r"\d+\.\d{1,2}\.\d{1,2}$"
        for goods_msg in goods_iter:
            if re.match(date_re_str, goods_msg):
                bill_date_str = goods_msg.strip()
                break

        return bill_date_str


class Cashier(Classify):
    def __init__(self, goods):
        super().__init__(goods)

    def get_goods_type_list(self):
        type_discounts = self.get_discounts()
        type_discounts = type_discounts if type_discounts else {}
        goods_type_list = [
            {"Promotional_goods" : GOODS_TYPE_MAP.get(goods_type),
             "discounts": float(discounts)}
            for goods_type, discounts in type_discounts.items()]
        return goods_type_list

    def map(self):
        total_price = 0
        goods_list = self.get_goods()
        goods_type_list = self.get_goods_type_list()
        for items in goods_list:
            goods_name = items.get("goods_name")
            old_total_price = items.get("total_price")
            tmp_total_price = old_total_price
            for goods_type_map in goods_type_list:
                if goods_name not in goods_type_map.get("Promotional_goods", []):
                    continue
                tmp_total_price = old_total_price * goods_type_map.get("discounts", 1)

            total_price += tmp_total_price
        return total_price

    def bill(self):
        tmp_total_price = self.map()
        coupon = self.get_coupon()
        actual_price = tmp_total_price - coupon.get("condition") if \
            (coupon and (coupon.get("remit") <= tmp_total_price)) else \
            tmp_total_price

        return "%.2f" % actual_price


# TODO optimization: all source date should multi-Progress like mapReduce


if __name__ == "__main__":
    pass
