"""
Forms for the `users` app.

Handles Django forms for user registration and editing profile details.
"""

from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth.models import User


class ProfileEditForm(ModelForm):
    """
    Form for editing basic profile information.

    Fields
    ------
    title : str
        User's title
    displayname : str
        User's display name.
    image : CloudinaryField
        User's profile avatar
    phone : int
        User's contact number.
    home_address : str
        User's home address.
    """    
    phone = forms.IntegerField(label='Contact Number',
                            widget=forms.TextInput(attrs={'placeholder': 'E.g. 07512345679',
                                                          'pattern': "^[0-9]{10,15}$",
                                                          'title': 'Phone number must be between 10 and 15 digits.',
                                                          }),)

    class Meta:
        model = Profile
        fields = ['title', 'displayname', 'image', 'phone', 'home_address']


class MainSignupForm(UserCreationForm):
    """
    Form for creating a new user account.

    Extends Django's built-in UserCreationForm to include
    additional fields and validation.

    Fields
    ------
    username : str
        The chosen username.
    email : str
        User's email address (must be unique).
    first_name : str
        User's first name.
    last_name : str
        User's last name.
    password1 : str
        User's chosen password.
    password2 : str
        Password confirmation.
    role : str
        Hidden field used to capture user type (driver, passenger).
    """    
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    role = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        """
        Validate that the provided email is unique.

        An error is raised if the email is already registered on another account.

        Returns
        -------
        str
            The cleaned email address.
        """        
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use by another user.")
        
        return email


class DriverEditForm(ModelForm):
    """
    Form for editing driver-specific profile details.

    Fields
    ------
    experience : int
        Years of driving experience.
    """    
    class Meta:
        model = DriverProfile
        fields = ['experience']
        labels = {'experience': 'Years of driving experience'}

class ManagerEditForm(ModelForm):
    """
    Form for editing manager-specific profile details.

    Fields
    ------
    experience : int
        Years of customer service experience.
    """    
    class Meta:
        model = ManagerProfile
        fields = ['experience']
        labels = {'experience': 'Years of customer service'}

class PassengerEditForm(ModelForm):
    """
    Form for editing passenger-specific profile details.

    Fields
    ------
    emergency_name : str
        Emergency contact name.
    emergency_phone : str
        Emergency contact phone number.
    """    
    class Meta:
        model = PassengerProfile
        fields = ['emergency_name', 'emergency_phone']


class ProfileSettingsForm(ModelForm):
    """
    Form for updating account settings.

    Fields
    ------
    email : str
        Updated email address for the user.
    """    
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        """
        Validate that the provided email is unique.

        An error is raised if the email is already registered on another account.

        Returns
        -------
        str
            The cleaned email address.
        """        
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use by another user.")
        
        return email