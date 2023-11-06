
from django import forms
class ContactUsForm(forms.Form):
   #name = forms.CharField(required=False)
   #email = forms.EmailField()
   message = forms.CharField(max_length=1000)

class ConnectionForm(forms.Form):
   identification = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), max_length=100)
   password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), max_length=100)

class NewAccountForm(forms.Form):
   identification = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), max_length=100)
   password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), max_length=100)
   email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}), max_length=100)
   confirmPassword = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), max_length=100)
   #serial = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), max_length=100)

class ForgottenPassword(forms.Form):
   email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}), max_length=100)

class NewPassword(forms.Form):
   newPassword = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), max_length=100)
   confirmPassword = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), max_length=100)