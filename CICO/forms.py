
from django import forms
class ContactUsForm(forms.Form):
   #name = forms.CharField(required=False)
   #email = forms.EmailField()
   message = forms.CharField(max_length=1000)

class ConnectionForm(forms.Form):
   indentification = forms.CharField(max_length=100)
   password = forms.CharField(max_length=100)