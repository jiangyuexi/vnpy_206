# -*- coding: utf-8 -*-
# @Time    : 2019/9/14 19:19
# @Author  : 蒋越希
# @Email   : jiangyuexi1992@qq.com
# @File    : data_recorder.py
# @Software: PyCharm
import sys
sys.path.append("/home/jiangyx/vnpy_206/vnpy")
from time import sleep

import logging

from vnpy.app.cta_strategy.base import EVENT_CTA_LOG
from vnpy.app.data_recorder.ui.no_widget import ConnectNoDialog
from vnpy.event import EventEngine
from vnpy.trader.constant import Exchange

from vnpy.trader.engine import MainEngine


# from vnpy.gateway.bitmex import BitmexGateway
# from vnpy.gateway.futu import FutuGateway
# from vnpy.gateway.ib import IbGateway
# from vnpy.gateway.ctp import CtpGateway
# from vnpy.gateway.femas import FemasGateway
# from vnpy.gateway.tiger import TigerGateway
# from vnpy.gateway.oes import OesGateway
from vnpy.gateway.okex import OkexGateway
from vnpy.gateway.huobi import HuobiGateway
# from vnpy.gateway.bitfinex import BitfinexGateway
# from vnpy.gateway.onetoken import OnetokenGateway
from vnpy.gateway.okexf import OkexfGateway
# from vnpy.gateway.xtp import XtpGateway
from vnpy.gateway.hbdm import HbdmGateway

from vnpy.app.data_recorder import DataRecorderApp
from vnpy.trader.setting import SETTINGS

SETTINGS["log.active"] = True
SETTINGS["log.level"] = logging.INFO
SETTINGS["log.console"] = True


def main():
    """"""
    # 创建 QApplication  对象 并进行初始化

    # 事件引擎
    event_engine = EventEngine()
    # 把事件引擎附加到主引擎里
    main_engine = MainEngine(event_engine)
    main_engine.write_log("主引擎创建成功")

    log_engine = main_engine.get_engine("log")
    event_engine.register(EVENT_CTA_LOG, log_engine.process_log_event)
    main_engine.write_log("注册日志事件监听")


    # 添加火币的交互通道
    # main_engine.add_gateway(HuobiGateway)
    # sleep(1)
    # main_engine.add_gateway(BitfinexGateway)
    # main_engine.add_gateway(OnetokenGateway)
    main_engine.add_gateway(OkexGateway)
    sleep(1)
    main_engine.add_gateway(OkexfGateway)

    # main_engine.add_gateway(HbdmGateway)
    # 把 app 保存到 apps 和 engines 里
    sleep(1)
    data_recorder_app = main_engine.add_app(DataRecorderApp)

    sleep(2)
    # 获取所有交易通道
    gateway_names = main_engine.get_all_gateway_names()
    for name in gateway_names:
        # 连接火币平台
        connect = ConnectNoDialog(main_engine=main_engine, gateway_name=name)
        connect.connect()
        sleep(2)

    sleep(20)

    for tick in data_recorder_app.tick_recordings.keys():
        data_recorder_app.add_tick_recording(tick)

    for bar in data_recorder_app.bar_recordings.keys():
        data_recorder_app.add_bar_recording(bar)

    while True:
        # 一天
        sleep(100000000)


if __name__ == "__main__":
    main()
