from django.forms import Form
from django import forms


class UserContactForm(Form):
    name = forms.CharField(max_length=100, label='Full Name', widget=forms.TextInput(
        attrs={'placeholder': 'Your Name'}))
    email = forms.EmailField(label='Email Address', widget=forms.EmailInput(
        attrs={'placeholder': 'Your Email'}))
    phone = forms.CharField(label='Contact Number',
                            widget=forms.TextInput(attrs={'placeholder': 'E.g. 07512345679',
                                                          'pattern': "^[0-9]{10,15}$",
                                                          'title': 'Phone number must be between 10 and 15 digits.',
                                                          }),
                            )
    message = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Enter Your Message', 'rows': 3}), label='Message')    
    
    receive_copy = forms.BooleanField(required=False, label="Receive a copy of this enquiry")

