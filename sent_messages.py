
from dblink import Pydb
from random import randint
from datetime import datetime
import hashlib
import requests, json
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
    # message = '这是一条营销短信，可以访问百度http://www.baidu.com'
    # send_phone_message(mobile,message)

    table = 'inla'
    pydb = Pydb()
    sql = "SELECT phone FROM %s WHERE phone<>'' ORDER BY id ASC LIMIT %s" % (table,limit)
    emails = pydb.query(sql)
    elist = []
    for e in emails:
        if ';' in e:
            es = e.split(';')
            elist.extend(es)
        else:
            elist.append(e)


if __name__ == '__main__':
    sent_messages()
