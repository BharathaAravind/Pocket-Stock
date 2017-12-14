from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelChoiceField, widgets
from django.forms.extras.widgets import SelectDateWidget

from stocks.models import TransactionModel, StockStatusModel, StockProfileModel

class RegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username','email','first_name','last_name', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields =(
                 'username',
                 'first_name',
                 'last_name',
                 'email',
                 'password1',
                 'password2'
        )

    def save(self, commit=True):
        user= super(RegistrationForm, self).save(commit=False)
        user.first_name= self.cleaned_data['first_name']
        user.last_name= self.cleaned_data['last_name']
        user.email=self.cleaned_data['email']

        if commit:
            user.save()

        return user


class TransactionAddForm(forms.Form):
    """Form for a user creating a transaction"""
    #The amount of money that the user spent on the stock
    amountSpent = forms.DecimalField(max_digits=8, decimal_places=2)
    #The number of stocks purchased
    numberPurchased = forms.IntegerField()
    #The date on which the stocks were purchased
    datePurchased = forms.DateField(widget=SelectDateWidget(years=range(2007, 2020)))
    #The company that the stock purchased was for
    whichStock = ModelChoiceField(queryset=StockProfileModel.objects.all())


    class Meta:
        model = TransactionModel
        fields = (
            'amountSpent',
            'numberPurchased',
            'datePurchased',
            'whichStock'
            )

    def save(self, user):

        transaction = TransactionModel()
        transaction.user = user
        transaction.amountSpent = self.cleaned_data['amountSpent']
        transaction.numberPurchased = self.cleaned_data['numberPurchased']
        transaction.datePurchased = self.cleaned_data['datePurchased']
        transaction.whichStock = self.cleaned_data['whichStock']
        transaction.save()
