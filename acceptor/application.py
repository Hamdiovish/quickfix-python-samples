"""FIX Application"""
import sys
import quickfix as fix
import logging
import time
from model import Field
from model.Message import Base, Types, __SOH__
from model.logger import setup_logger
import quickfix44 as fix44
from helpers import *

setup_logger('logfix', 'Logs/message.log')
logfix = logging.getLogger('logfix')

class Application(fix.Application):
    """FIX Application"""
    sessionID = None
    OrderID = 0
    marketSubscribers = {'EURUSD':[]}
    """ symbol : [sessionID] """

    def onCreate(self, sessionID):
        """onCreate"""
        return

    def onLogon(self, sessionID):
        self.sessionID = sessionID
        """onLogon"""
        return

    def onLogout(self, sessionID):
        """onLogout"""
        return

    def toAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.debug("toAdmin >> %s" % msg)
        return

    def fromAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.debug("fromAdmin << %s" % msg)
        return

    def toApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.debug("toApp >> %s" % msg)
        return

#    def fromApp(self, message: fix44.Message, session_id):

    def fromApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.debug("fromApp << %s" % msg)

        msg_type = get_header_value(message, fix.MsgType())
        if msg_type in (
            fix.MsgType_MarketDataRequest
        ):
            self.onMessage(message, sessionID)
        return
    

    def onMessage(self, message, sessionID):
        msg_type = get_header_value(message, fix.MsgType())
        if msg_type == fix.MsgType_MarketDataRequest:
            group = fix44.MarketDataRequest.NoRelatedSym()
            group_count = get_field_value(message, fix.NoRelatedSym())
            for group_idx in range(1, group_count + 1):
                message.getGroup(group_idx, group)
                symbol = get_field_value(group, fix.Symbol())
                if not sessionID.getTargetCompID().getString() in self.marketSubscribers[symbol]:
                    self.marketSubscribers[symbol].append(sessionID.getTargetCompID().getString())

    def run(self):
        """Run"""
        while 1:
            time.sleep(2)
            for symbol in self.marketSubscribers:
                if len(self.marketSubscribers[symbol])>0:
                    print(symbol," : "," ".join(str(x) for x in self.marketSubscribers[symbol]), " will receive ticks fake for ",symbol," market")


#2021-03-14 23:56:55,976 : fromApp << 8=FIX.4.4|9=115|35=V|34=2|49=TESTINI|52=20210314-22:56:55.975|56=TESTACC|146=1|55=EURUSD|262=1|263=1|264=3|265=1|267=2|269=0|269=1|10=064|
