from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
import forms
import datetime
import models
from django.contrib.auth.decorators import login_required

# Create your views here.


def user(request):
    cur_date = datetime.datetime.now()
    cur_time= cur_date.strftime("%d.%m.%Y %I:%M")
    cur_hour = cur_date.hour
    print cur_hour
    if request.method == 'POST':
        form = forms.DUserForm(request.POST)
        print form
        if form.is_valid():
            data = form.cleaned_data
            item=data['item']
            whom=data['whom']
            e_mail=data['e_mail']
            byr=data['byr']
            byn=data['byn']
            comment=data['comment']
            models.DUserModel.objects.create(item=item, whom=whom, e_mail=e_mail, byr=byr, byn=byn, comment=comment)
            return render(request, 'confirmation.html', {})
        else:
            return render(request, 'duserform.html', {'form':form})

    else:
        if 13 <= cur_hour <= 15:
            status = True
        else:
            status = False
        status = 14  # zaplatka
        return render(request, 'duserform.html', {'form': forms.DUserForm(), 'status': status})


@login_required(login_url='/accounts/login/')
def ordertable(request):
    orders = models.DUserModel.objects.all()
    summ_in_byr = 0
    summ_in_byn = 0
    itog = 0
    for order in orders:
        summ_in_byn += order.byn
        summ_in_byr += order.byr
    itog = summ_in_byn + summ_in_byr / 10000
    return render(request, 'orderstable.html', {'orders':orders, 'byn':summ_in_byn, 'bur':summ_in_byr, 'itog': itog})


def edit(request, pk):
    if request.method == 'POST':
        form=forms.DUserForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            my_object = models.DUserModel.objects.get(pk=pk)
            my_object.item = data['item']
            my_object.whom = data['whom']
            my_object.e_mail = data['e_mail']
            my_object.byn = data['byn']
            my_object.byr = data['byr']
            my_object.save()
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


def delete(request, pk):
    try:
        TaskModel.objects.get(pk=pk).delete()
    except exceptions.ObjectDoesNotExist:
        return redirect('index')
    return redirect('index')
