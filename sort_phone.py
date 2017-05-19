from dblink import Pydb
import re
import logging
logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='debug.log',
    filemode='a')




def get_phone(phoneStr):
    phoneStr = phoneStr.strip().replace(' ','')
    if not phoneStr:
        return ''

    # clean format
    # phoneStr = phoneStr.replace('-','#')
    # phoneStr = phoneStr.replace('(','#')
    # phoneStr = phoneStr.replace(')','#')
    # phoneStr = phoneStr.replace('）','#')
    # phoneStr = phoneStr.replace('（','#')
    # phoneStr = phoneStr.replace('.','#')
    phoneStr = re.sub(r'[\.\-\(\)）（]+','#',phoneStr)

    relist = [
        r"(1#[0-9]{3}#[0-9]{3}#[0-9]{4})",
        r"([0-9]{3}#[0-9]{3}#[0-9]{4})",
        r"([0-9]{10,11})"
    ]

    phones = []
    for res in relist:
        result = re.findall(res,phoneStr)
        phones.extend(result)
        for s in result:
            phoneStr.replace(s,'')

    return ';'.join(phones).replace('#','')


def sort_phone():
    table = 'inla'
    pydb  = Pydb()
    numArr = pydb.get_count(table)
    for n in xrange(numArr):
        try:
            items = pydb.filter(table,{'id':n+1})
            phones = get_phone(items[0]['phone'])
            pydb.update(table,{'phone':phones},{'id':items[0]['id']})
            logging.info('update success:%s' % items[0]['id'])
        except Exception as e:
            logging.info('update failed:%s' % items[0]['id'])



if __name__ == '__main__':
    sort_phone()
