from django import forms


class CreateTokenForm(forms.Form):
    Quantity = forms.IntegerField()
    Disposable = forms.BooleanField()
