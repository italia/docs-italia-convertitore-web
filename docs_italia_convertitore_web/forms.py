from django import forms

class ItaliaConverterForm(forms.Form):
    email = forms.EmailField()
    file = forms.FileField()
    monospace = forms.BooleanField(required=False)


