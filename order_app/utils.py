# -*- coding=utf-8 -*-
import smtplib


def send_mail_to_user(**kwargs):
    mail = kwargs['mail']
    item_to_buy = kwargs['item']
    comment = kwargs['comment']
    text = 'Your order was changed by administrator. You new order is "{}"'.format(item_to_buy)
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
    server.sendmail("djangotest14@yandex.ru", mail, message)
    server.quit()


def send_mail_to_admin(**kwargs):
    item = kwargs['item']
    whom = kwargs['whom']
    mail = kwargs['mail']
    text = 'You received a new order from {}. Item is ordered - "{}"'.format(whom, item)
    server = smtplib.SMTP_SSL("smtp.yandex.ru:465")
    server.ehlo()
    server.login("djangotest14@yandex.ru", "!Qaz@Wsx")
    message = "\r\n".join([ \
        "From: Dinner request", \
        "To: You", \
        "Subject: Order details", \
        "", \
        "{}".format(text) \
        ])
    server.sendmail("djangotest14@yandex.ru", 'djangotest14@yandex.ru', message)
    server.quit()