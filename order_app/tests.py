from simplejson import JSONEncoder

from django.contrib.sessions.models import Session
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.test import TestCase
from mock import patch
from django.core import mail
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import models
# Create your tests here.


class EmailTest(TestCase):

    def test_send_email(self):
        # Send message.
        mail.send_mail('Subject here', 'Here is the message.',
            'from@example.com', ['to@example.com'],
            fail_silently=False)

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Subject here')


def test_send_email(*args, **kwargs):
    # Send message.
    return 'OK'


from django.core import serializers


def new_render(a, b, c):
    result = json.dumps(c)
    return HttpResponse(result)


def new_render_2(a, b, c):
    result = json.dumps([c['byr'], c['byn'], c['itog']], cls=DjangoJSONEncoder)
    return HttpResponse(result)


def new_cur_time():
    return 14


class MyTests(TestCase):

    @patch('order_app.views.render', new=new_render)
    @patch('order_app.views.send_mail_to_admin', new=test_send_email)
    def test_order_creation(self):
        with patch('order_app.views.render', new=new_render):
            test_data = {
                'item': 'test_item',
                'whom': 'test_user',
                'e_mail': 'test_mail@test.ru',
                'byr': 10,
                'byn': 1,
                'comment': 'test_comment'
            }
            result = self.client.post('/', test_data)
            content = json.loads(result.content)
            orders = models.DUserModel.objects.all()
            order = orders.get()
            self.assertEquals(content['message'], 'Your order test_item is processing')
            self.assertEqual(orders.count(), 1)
            self.assertEqual(order.item, 'test_item')
            self.assertEqual(order.e_mail, 'test_mail@test.ru')
            self.assertEqual(order.whom, 'test_user')

    @patch('order_app.views.render', new=new_render_2)
    def test_summ_orders(self):
        my_object = models.DUserModel.objects.create(
            item= 'test_item',
            whom= 'test_user',
            e_mail= 'test_mail@test.ru',
            byr= 10000,
            byn= 1,
            comment= 'test_comment'
        )
        print my_object
        user = User.objects.create_user('test', 'test@test.ru', 'test11test')
        user.is_superuser = True
        user.save()
        self.client.login(username='test', password=r'test11test')
        result=self.client.get('/orders/')
        content = json.loads(result.content)
        self.assertEqual(content[2], 2.0)

    @patch('order_app.views.send_mail_to_user', new=test_send_email)
    @patch('order_app.views.render', new=new_render_2)
    def test_edit_ok(self):
        my_object = models.DUserModel.objects.create(
            item='test_item',
            whom='test_user',
            e_mail='test_mail@test.ru',
            byr=10000,
            byn=1,
            comment='test_comment'
        )
        user = User.objects.create_user('test', 'test@test.ru', 'test11test')
        user.is_superuser = True
        user.save()
        self.client.login(username='test', password=r'test11test')
        new_data = {
            'item':'test_item',
            'whom':'test_user',
            'e_mail':'test_mail@test.ru',
            'byr':10000,
            'byn':1,
            'comment':'test_comment_new'
        }
        result = self.client.post('/order/1/edit/', new_data)
        my_new_query = models.DUserModel.objects.all()
        my_new_object = my_new_query.get()
        self.assertNotEqual(my_new_object.comment, my_object.comment)
        self.assertEqual(my_new_object.comment, 'test_comment_new')

    @patch('order_app.views.send_mail_to_user', new=test_send_email)
    @patch('order_app.views.render', new=new_render_2)
    def test_delete_ok(self):
        my_object = models.DUserModel.objects.create(
            item='test_item',
            whom='test_user',
            e_mail='test_mail@test.ru',
            byr=10000,
            byn=1,
            comment='test_comment'
        )
        user = User.objects.create_user('test', 'test@test.ru', 'test11test')
        user.is_superuser = True
        user.save()
        self.client.login(username='test', password=r'test11test')
        result = self.client.post('/order/1/delete/')
        my_new_query = models.DUserModel.objects.all()
        self.assertEqual(my_new_query.count(), 0)
