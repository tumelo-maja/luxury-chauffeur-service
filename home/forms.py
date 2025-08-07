from django.forms import Form
from django import forms
from phonenumber_field.formfields import PhoneNumberField

class UserContactForm(Form):
    name = forms.CharField(max_length=100, label='Full Name', widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    email = forms.EmailField(label='Email Address', widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}))
    phone = PhoneNumberField(label='Contact Number', widget=forms.TextInput(attrs={'placeholder': 'Your Contact Number'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter Your Message', 'rows': 3}), label='Message')
