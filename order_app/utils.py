# -*- coding=utf-8 -*-
import smtplib


def send_mail_test(**kwargs):
    mail = kwargs['mail']
    item_to_buy = kwargs['item']
    comment = kwargs['comment']
    text = 'Your order was changed by administrator. You new order is "{}"'.format(item_to_buy)
    print comment, type(comment), len(comment)
    if len(comment) != 0:
        text += ' with comment "{}"'.format(comment)
    server = smtplib.SMTP_SSL("smtp.yandex.ru:465")
    server.ehlo()
    server.login("djangotest14@yandex.ru", "!Qaz@Wsx")
    message = "\r\n".join([ \
        "From: Dinner order", \
        "To: You", \
        "Subject: Order details", \
        "", \
        "{}".format(text) \
        ])
    server.sendmail("djangotest14@yandex.ru", "mix-87@yandex.ru", message)
    server.quit()

