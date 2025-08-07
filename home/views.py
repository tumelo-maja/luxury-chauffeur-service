from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
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

            subject = f"Enquiry from {name}"
            body = f"Name: {name}\nEmail: {email}\nContact Number: {phone}\nMessage: {message}"
            recipient_email = settings.DEFAULT_FROM_EMAIL
            # send_mail(subject, body, email, [recipient_email])
            email_thread = threading.Thread(target=send_email_async, args=(subject, body, email, recipient_email))
            email_thread.start()

            context = {
                'message': "Thank you for your enquiry! We will get back to you soon.",
            }

            return render(request, 'partials/success_message.html', context)
    else:
        form = UserContactForm()

    context ={'form': form,}

    return render(request, 'home/contact.html', context)

def send_email_async(subject, body, from_email, to_email):
    send_mail(subject, body, from_email, to_email)
    
def success_view(request):
    return render(request, 'success.html')
