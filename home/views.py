from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import os
import threading
from .forms import UserContactForm


def home_view(request):
    return render(request, 'home/home.html')


def contact_form_view(request):
    if request.method == 'POST':
        form = UserContactForm(request.POST)
        if form.is_valid():

            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']
            receive_copy = form.cleaned_data['receive_copy']

            context = {
                        'enquiry': {
                            'name': name,
                            'email': email,
                            'phone': phone,
                            'message': message,
                        },
                        'subtitle': 'You have received a new enquiry from the website:',
                        'recipient': 'Admin',
                    }
            
            html_message = render_to_string('home/enquiry-email.html', context)
            text_message = strip_tags(html_message)


            # email for site admin
            send_mail(
                subject='New Website Enquiry from ' + name,
                message=text_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL,],
                html_message=html_message,
            )  

            if receive_copy:
                context['recipient']= name
                context['subtitle']= 'Thank you for contacting Lux Chauffeurs. We have received your enquiry and will get back to you as soon as possible.'
                
                html_message = render_to_string('home/enquiry-email.html', context)
                text_message = strip_tags(html_message)
                send_mail(
                    subject='Copy of Your Enquiry with Lux Chauffeurs',
                    message=text_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    html_message=html_message,
                )                 

            return render(request, 'partials/success_message.html')
    else:
        form = UserContactForm()

    context ={'form': form,}

    return render(request, 'home/contact.html', context)

