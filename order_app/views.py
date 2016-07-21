import exceptions
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
import forms
import datetime
import models
from django.contrib.auth.decorators import login_required
from utils import send_mail_to_user, send_mail_to_admin, cur_hour
import copy

# Create your views here.


def user(request):

    if request.method == 'POST':
        form = forms.DUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            item=data['item']
            whom=data['whom']
            e_mail=data['e_mail']
            byr=data['byr']
            byn=data['byn']
            comment=data['comment']
            models.DUserModel.objects.create(item=item, whom=whom, e_mail=e_mail, byr=byr, byn=byn, comment=comment)
            send_mail_to_admin(whom=whom, item=item, mail=e_mail)
            return render(request, 'confirmation.html', {'message': 'Your order %s is processing' % item})
        else:
            return render(request, 'duserform.html', {'form':form})

    else:
        if 13 <= cur_hour() <= 15:
            status = True
        else:
            status = False
        # status = True  # zaplatka
        return render(request, 'duserform.html', {'form': forms.DUserForm(), 'status': status})


@login_required
def ordertable(request):
    orders = models.DUserModel.objects.all()
    summ_in_byr = 0
    summ_in_byn = 0
    itog = 0
    for order in orders:
        if order.byn is None:
            order.byn = 0
        elif order.byr is None:
            order.byr = 0
        summ_in_byn += float(order.byn)
        summ_in_byr += int(order.byr)
    itog = summ_in_byn + summ_in_byr / 10000.0
    return render(request, 'orderstable.html', {'orders': orders, 'byn': summ_in_byn, 'byr': summ_in_byr, 'itog': itog})


@login_required(login_url='/accounts/login/')
def edit(request, pk):
    if request.method == 'POST':
        form=forms.DUserForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            my_object = models.DUserModel.objects.get(pk=pk)
            my_old_object = copy.copy(my_object)
            my_object.item = data['item']
            my_object.whom = data['whom']
            my_object.e_mail = data['e_mail']
            my_object.byn = data['byn']
            my_object.byr = data['byr']
            my_object.comment = data['comment']
            my_object.save()
            if my_old_object.comment != my_object.comment or my_old_object.item != my_object.item:
                send_mail_to_user(mail=my_object.e_mail, item=my_object.item, comment=my_object.comment)
            return redirect('ordertable')
        else:
            my_object = forms.DUserForm.objects.get(pk=pk)
            return render(request, 'editform.html', {'form':forms.DUserForm(initial={
                'item': my_object.item,
                'whom': my_object.whom,
                'e_mail':my_object.e_mail,
                'byr':my_object.byr,
                'byn':my_object.byn,
                'comment':my_object.comment,
            }), 'pk': pk})

    else:
        my_object = models.DUserModel.objects.get(pk=pk)
        return render(request, 'editform.html', {'form': forms.DUserForm(initial={
            'item': my_object.item,
                'whom': my_object.whom,
                'e_mail':my_object.e_mail,
                'byr':my_object.byr,
                'byn':my_object.byn,
                'comment':my_object.comment
            }), 'pk': pk})


@login_required(login_url='/accounts/login/')
def delete(request, pk):
    try:
        my_object = models.DUserModel.objects.get(pk=pk)
        email = my_object.e_mail
        my_object.delete()
        send_mail_to_user(mail=email, item=None, comment=None)
    except ObjectDoesNotExist:
        return redirect('ordertable')
    return redirect('ordertable')
