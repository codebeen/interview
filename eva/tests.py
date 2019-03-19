#!/usr/bin/env python
# -*- coding:utf-8 -*-
import unittest
# from fsm import FsmAccess
# from mock import Mock
from cashier import Cashier


class CashierTest(unittest.TestCase):

    def test_bill_01(self):
        self.pile_data= u"2013.11.11 | 0.7 | 电子\n1 * ipad : 2399.00\n1 * " \
                u"显示器 : 1799.00\n12 * 啤酒 : 25.00\n5 * 面包 : " \
                u"9.00\n2013.11.11\n2014.3.2 1000 200"
        cashier_obj = Cashier(self.pile_data)
        ret = cashier_obj.bill()
        self.assertEqual(ret, '3083.60')

    def test_bill_02(self):
        self.pile_data= u"3 * 蔬菜 : 5.98\n8 * 餐巾纸 : 3.20\n2014.01.01 输出\n"
        cashier_obj = Cashier(self.pile_data)
        ret = cashier_obj.bill()
        self.assertEqual(ret, '43.54')

    # TODO other methds mock ut
