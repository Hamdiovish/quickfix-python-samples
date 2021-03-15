#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import sys
# from datetime import datetime
import quickfix as fix
import time
import logging
from model.logger import setup_logger
from model import Field
from model.Message import __SOH__
import quickfix44 as fix44

# Logger
setup_logger('logfix', 'Logs/message.log')
logfix = logging.getLogger('logfix')


class Application(fix.Application):
    """FIX Application"""

    def __init__(self):
        super().__init__()
        self.exec_id = 0

    def onCreate(self, sessionID):
        self.sessionID = sessionID
        return
    def onLogon(self, sessionID):
        self.sessionID = sessionID
        self.send_mkt_data_req("EURUSD")
        return
    def onLogout(self, sessionID): 
        return

    def toAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("toAdmin >> %s" % msg)
        return
    def fromAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("fromAdmin << %s" % msg)
        return
    def toApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("toApp >> %s" % msg)
        return
    def fromApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("fromApp << %s" % msg)
        self.onMessage(message, sessionID)
        return

   
    def onMessage(self, message, sessionID):
        """Processing application message here"""
        pass

    def run(self):
        """Run"""
        while 1:
            time.sleep(2)

    def send_mkt_data_req(self, symbol):
        """
        :param symbol: str
        """
        print("send_mkt_data_req: ",symbol)
        message = fix44.MarketDataRequest()
        message.setField(fix.MDReqID(self.next_id()))
        message.setField(
            fix.SubscriptionRequestType(
                fix.SubscriptionRequestType_SNAPSHOT_PLUS_UPDATES
            )
        )
        message.setField(fix.MarketDepth(3))

        message.setField(fix.MDUpdateType(fix.MDUpdateType_INCREMENTAL_REFRESH))

        symbol_group = fix44.MarketDataRequest.NoRelatedSym()
        symbol_group.setField(fix.Symbol(symbol))
        message.addGroup(symbol_group)

        types = fix44.MarketDataRequest.NoMDEntryTypes()
        types.setField(fix.MDEntryType(fix.MDEntryType_BID))
        message.addGroup(types)

        types = fix44.MarketDataRequest.NoMDEntryTypes()
        types.setField(fix.MDEntryType(fix.MDEntryType_OFFER))
        message.addGroup(types)

        fix.Session_sendToTarget(message, self.sessionID)

    def next_id(self):
        self.exec_id = self.exec_id + 1
        return str(self.exec_id)

#2021-03-14 23:56:55,975 : toApp >> 8=FIX.4.4|9=115|35=V|34=2|49=TESTINI|52=20210314-22:56:55.975|56=TESTACC|146=1|55=EURUSD|262=1|263=1|264=3|265=1|267=2|269=0|269=1|10=064|
