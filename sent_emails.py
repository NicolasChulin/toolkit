from dblink import Pydb
import smtplib
from email.mime.text import MIMEText
from email.header import Header

EMAIL_HOST = 'smtp.mxhichina.com'
EMAIL_HOST_USER = 'service@yunye123.com'
EMAIL_HOST_PASSWORD = 'Yunye0128'



def sent_email():
    email = 'hitgzms@163.com'
    sent_html_email(email)

def get_email_template():
    message_txt = u"""
        <p>尊敬的客户，您好！</p>
        <p></p>
        <p>this is a text</p>
        <p></p>
        <p>武汉云页移动科技有限公司</p>
        <p>联系电话：027-87345335</p>
    """
    return message_txt


def sent_html_email(email_address):

    sender = EMAIL_HOST_USER
    receivers = [email_address]
    print(receivers)

    mail_msg = get_email_template()
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header("武汉云页移动科技", 'utf-8')
    message['To'] =  Header("云页", 'utf-8')

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
