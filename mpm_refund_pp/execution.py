#! usr/bash/python3
# -*- coding=utf-8 -*-
# author: Josh
# date: 11 Jun 2020

"""The script is to realize MPM refund auto.
    RELEASE YOUR HANDS
"""

import main

print("-" * 50)
print("环境选项[PP,PR]")
print("网络连接方法:[0,1]// 0=>办公室网络, 1=>vpn网络")
print("订单号输入规则：逗号隔开无空格，且每个orderid需要有单引号")
print("-" * 50)
print(" ")

env = input('environment = ')
connection = str(input('connection method = '))
orders = input("请输入你要退的订单号: ")

refund = main.MiniRefund(env, connection, orders)

res = refund.send_request()






