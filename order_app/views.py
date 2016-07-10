from django.shortcuts import render
import forms
import datetime

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
        else:
            return render(request, 'duserform.html', {'form':form})

    else:
        if 13 <= cur_hour <= 15:
            status = True
        else:
            status = False
        return render(request, 'duserform.html', {'form': forms.DUserForm(), 'status': status})
