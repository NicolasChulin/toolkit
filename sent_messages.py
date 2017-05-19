
from dblink import Pydb
from random import randint
from datetime import datetime
import hashlib
import requests, json,math
import logging
logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='debug.log',
    filemode='a')


APPKEY = '94477a21ee1bdc233624f6bb8a916da4'
APPID = '1400012785'


def get_random_num(num):
    nums = []
    for n in range(num):
        nums.append(str(randint(0,9)))
    return ''.join(nums)


def get_limit(curpage,ppnum):
    start = (curpage-1)*ppnum
    return '%s,%s' % (start,ppnum)


def get_mess_config(mobile):
    strAppkey = APPKEY
    random = get_random_num(6)
    time = int(datetime.timestamp(datetime.now()))
    stri = 'appkey=%s&random=%s&time=%s&mobile=%s' % (strAppkey,random,time,mobile)
    sig = hashlib.sha256(stri.encode('utf-8')).hexdigest()
    url = 'https://yun.tim.qq.com/v5/tlssmssvr/sendsms'
    params = {'sdkappid': APPID, 'random': random}

    return {
        'time':time,
        'sig':sig,
        'url':url,
        'params':params
    }


def send_phone_message(mobile):
    conf = get_mess_config(mobile)
    body = {
        "tel": {
            "nationcode": "86", # america is 1
            "mobile": mobile
        },
        "type": 1,
        "tpl_id":1018,
        "params":params,
        "sig": conf['sig'],
        "time": conf['time'],
        "extend": "",
        "ext": ""
    }
    resp = requests.post(conf['url'], params=conf['params'], json=body)
    response = resp.json()
    if response['result'] == 0:
        logging.info('message sent success:%s....Success' % (mobile))
    else:
        logging.info('message sent failed:%s....Failed,code:%s,msg:%s' % (mobile,response['result'],response['errmsg']))




def sent_messages():
    # mobile = '18566268446'
    # send_phone_message(mobile)

    table = 'inla'
    ppnum = 100

    pydb = Pydb()
    num = pydb.get_count(table)
    allpage = math.ceil(num['num']/ppnum)
    for n in range(allpage):
        limit = get_limit(allpage,n+1,ppnum)
        sql = "SELECT phone FROM %s ORDER BY id ASC LIMIT %s" % (table,limit)
        phones = pydb.query(sql)
        for phone in phones:
            send_phone_message(phone['phone'])



if __name__ == '__main__':
    sent_messages()
