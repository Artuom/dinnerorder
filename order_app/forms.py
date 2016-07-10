from models import DUserModel
from django import forms


class DUserForm(forms.ModelForm):
    class Meta:
        model = DUserModel
        fields = '__all__'
