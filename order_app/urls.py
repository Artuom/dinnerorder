from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.user, name='user'),
    url(r'^orders', views.ordertable, name='ordertable'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^order/(?P<pk>[0-9]+)/delete/$', views.delete, name='delete'),
    url(r'^order/(?P<pk>[0-9]+)/edit/$', views.edit, name='edit'),
]
