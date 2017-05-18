from dblink import Pydb
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import logging

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='debug.log',
    filemode='w')


EMAIL_HOST = 'smtp.mxhichina.com'
EMAIL_HOST_USER = 'service@yunye123.com'
EMAIL_HOST_PASSWORD = 'Yunye0128'


def sent_email():
    print('start-end')
    return

    table = 'inla'
    pydb = Pydb()
    sql = "SELECT email FROM %s WHERE email<>''" % (table,limit)
    emails = pydb.query(sql)
    elist = []
    for e in emails:
        if ';' in e:
            es = e.split(';')
            elist.extend(es)
        else:
            elist.append(e)

    elen = len(elist)
    limits = [x for x in range(0,len+1,100)]
    if elen//100:
        limits.append(elen)

    ll = len(limits)
    for index,lim in enumerate(limits):
        if index < ll-1:
            sent_html_email(elist[lim:limits[index+1]])



def get_email_template():
    message_txt = """
        <p>尊敬的客户，您好！</p>
        <br>
        <p>this is a text</p>
        <br>
        <p>武汉云页移动科技有限公司</p>
        <p>联系电话：027-87345335</p>
    """
    return message_txt


def sent_html_email(email_address):

    sender = EMAIL_HOST_USER
    receivers = email_address

    mail_msg = get_email_template()
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header("云页科技", 'utf-8')
    message['To'] =  Header("user", 'utf-8')

    subject = '精彩推荐 云页科技'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(EMAIL_HOST, 25)
        smtpObj.login(EMAIL_HOST_USER,EMAIL_HOST_PASSWORD)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print('success!')
    except smtplib.SMTPException:
        print('fail')


if __name__ == '__main__':
    sent_email()
