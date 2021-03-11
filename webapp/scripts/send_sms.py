#! /usr/bin/python3

# pip3 install python-dotenv

import logging
from urllib.parse import urlencode, quote_plus
from urllib.request import urlopen
from xml.dom.minidom import parseString
import sqlalchemy as db
from sqlalchemy.exc import SQLAlchemyError

import os
from datetime import datetime as dt
from dotenv import load_dotenv
# from pathlib import Path    # env_path

from color_print import cprint, PrintException


# env_path = Path('.') / '.env'
# load_dotenv(dotenv_path=env_path)
load_dotenv()


class Websms(object):
    def __init__(self):
        self._username = ''
        self._password = ''
        self._fromName = ''
        self._isViber = False
        self._messId = []
        self._websmsLogger = logging.getLogger('websms')
        # fh = logging.FileHandler('websms-notify.log')
        # self._websmsLogger.addHandler(fh)

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, val):
        self._username = val

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, val):
        self._password = val

    @property
    def fromName(self):
        return self._fromName

    @fromName.setter
    def fromName(self, val):
        self._fromName = val

    @property
    def messId(self):
        return self._messId

    @property
    def isViber(self):
        return self._isViber

    @isViber.setter
    def isViber(self, val):
        boolVal = True if val else False
        self._isViber = boolVal

    def sendSMS(self, msg, phone):
        if self._username == '' or self._password == '':
            self._websmsLogger.error('Login or password is empty')
            return False
        elif msg == '':
            self._websmsLogger.error('You cannot send empty message')
            return False
        elif phone == '':
            self._websmsLogger.error('Non-empty list of recipients requires')
            return False
        else:
            msg = msg.encode('windows-1251')
            url = 'http://websms.ru/http_in5.asp'
            mode = 'SMS'
            if self._isViber:
                mode = 'VIBER'
            params = {'http_username': self._username, 'http_password': self._password, 'fromPhone': self._fromName, 'Message': msg, 'Phone_list': phone, 'format': 'XML', 'mode': mode}
            url = url + '?' + urlencode(params, quote_via=quote_plus)

            self._websmsLogger.debug('Send SMS with: %s' % url)
            try:
                response = urlopen(url)

                if response.code != 200:
                    self._websmsLogger.error('Falied send SMS: status %s - %s' % (response.code, response.read()))
                    return False

                xml = response.read()
                dom = parseString(xml)
                httpIn = dom.getElementsByTagName('httpIn')[0]
                error_num = httpIn.getAttributeNode('error_num').nodeValue
                if error_num != '0':
                    self._websmsLogger.error('Falied send SMS: server returned error_num %s' % error_num)
                    return False
                else:
                    sms = dom.getElementsByTagName('sms')
                    for node in sms:
                        msgId = node.getAttributeNode('message_id').nodeValue
                        if msgId is not None:
                            self._messId.append(msgId)

            except Exception as err:
                self._websmsLogger.error('Falied send SMS: %s' % err)
                return False

            self._websmsLogger.debug('the message was sent')
            return True

    def getStatus(self, msgId):
        result_id = 0
        url = 'http://websms.ru/http_out5.asp'
        params = {'http_username': self._username, 'http_password': self._password, 'message_id': msgId, 'format': 'XML'}
        url = url + '?' + urlencode(params, quote_via=quote_plus)

        self._websmsLogger.debug('Send Status request for message_id %s' % msgId)
        try:
            response = urlopen(url)

            if response.code != 200:
                self._websmsLogger.error('Falied Status request: status %s - %s' % (response.code, response.read()))
                return 0

            xml = response.read()
            dom = parseString(xml)
            sms = dom.getElementsByTagName('sms')
            for node in sms:
                result_id = int(node.getAttributeNode('result_id').nodeValue)
                break

        except Exception as err:
            self._websmsLogger.error('Falied Status request: %s' % err)

        return result_id

    def getLastStatus(self):
        if len(self._messId) > 0:
            return self.getStatus(self._messId[len(self._messId) - 1])
        else:
            return 0

    def getLastMessId(self):
        if len(self._messId) > 0:
            return self._messId[len(self._messId) - 1]
        else:
            return 0

    def clearMsg(self):
        self._messId.clear()


# Define the MySQL engine using MySQL Connector/Python
try:
    # pth = '{}/logs/error_sms.log'.format( os.environ["WORK_DIR_WEBAPP"])
    pth = '{}/logs/error_sms.log'.format(os.getenv("WORK_DIR_WEBAPP"))
    # pth = 'logs/error_sms.log'

    e = db.create_engine(
        'mysql+mysqlconnector://pythonuser:flaskdefault@localhost:3306/webappdb',
        echo=False)
    conn = e.connect()
    # meta = db.MetaData.reflect(True, bind=e)
    meta = db.MetaData(bind=e, reflect=True)
    customers_tb = meta.tables['customers']

    query = db.select([customers_tb]).where(customers_tb.c.isEnabled == 'Yes')
    res = conn.execute(query)
    # customers = res.fetchall()

    # websmslogin = os.environ["WEBSMS_LOGIN"]
    # websmspassword = os.environ["WEBSMS_PWD"]
    websmslogin = os.getenv("WEBSMS_LOGIN")
    websmspassword = os.getenv("WEBSMS_PWD")

    w = Websms()
    w.username = websmslogin
    w.password = websmspassword
    # w.isViber = False

    for row in list(res):
        cprint("PURPLE", "here")
        if not row.lastsenddate or row.lastsenddate < row.deliverydate:
            try:
                w.sendSMS(row.message, row.phone)
                lastsenddate = dt.now().strftime("%Y-%m-%d %H:%M:%S")
                lastMessageId = w.getLastMessId()
                status = w.getLastStatus()
                cprint('GREEN', "[{}] phone: {}, message: {}, lastMessageId: {}, status: {}".format(lastsenddate, row.phone, row.message, lastMessageId, status))

                query = db.update(customers_tb).where(customers_tb.c.id == row.id).values(lastsenddate=lastsenddate, lastMessageId=lastMessageId, status=status)
                res = e.execute(query)
                cprint("PURPLE", "res: {}".format(res))

                # print('message ID = %s' % w.getLastMessId())
                # print('Состояние последнего СМС-сообщения: %s' % w.getLastStatus())

            except SQLAlchemyError as exc:
                cprint("YELLOW", "Exception: {}".format(exc))
                PrintException(pth)

except Exception as exc:
    cprint("YELLOW", "Exception: {}".format(exc))
    PrintException(pth)
