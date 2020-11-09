from django import forms
from django.forms import ModelForm
from .models import Order, User, Refund
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm


class OrderCreateForm(ModelForm):
    amount = forms.IntegerField(label='', initial='1', min_value=1)

    class Meta:
        model = Order
        fields = ['amount', ]


class RefundCreateForm(ModelForm):
    class Meta:
        model = Refund
        fields = []


class UserCreateForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',
                  'email')
