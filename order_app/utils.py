# -*- coding=utf-8 -*-
import smtplib
import datetime

def send_mail_to_user(**kwargs):
    mail = kwargs['mail']
    item_to_buy = kwargs['item']
    comment = kwargs['comment']
    if comment is not None and item_to_buy is not None:
        text = 'Your order was changed by administrator. You new order is "{}"'.format(item_to_buy)
    else:
        text = 'Your order was deleted by administrator.'
    if comment is not None and len(comment) != 0:
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


def cur_hour():
    cur_date = datetime.datetime.now()
    cur_time = cur_date.strftime("%d.%m.%Y %I:%M")
    cur_hour = cur_date.hour
    return cur_hour