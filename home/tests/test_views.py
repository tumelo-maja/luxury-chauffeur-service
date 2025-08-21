from django.test import SimpleTestCase
from django.shortcuts import reverse
from unittest.mock import patch
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from ..forms import UserContactForm

class TestHomeView(SimpleTestCase):

    def test_home_page_uses_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response,'home/home.html')

    def test_home_page_contains_hero_section_heading_text(self):
        response = self.client.get('/')
        self.assertContains(response,'Experience Unrivaled Luxury', status_code=200)
    
    def test_home_page_contains_correct_section_headings(self):
        response = self.client.get('/')
        self.assertContains(response,'Our Services')
        self.assertContains(response,'Our Fleet')

    def test_home_page_contains_a_header_login_and_signup_buttons(self):
        response = self.client.get('/')
        self.assertContains(response, f'<a href="{reverse("account_login")}">Login</a>')
        self.assertContains(response, f'<a href="{reverse("signup_type")}">Signup</a>')


class TestContactFormView(SimpleTestCase):

    def setUp(self):
        self.contact_enquiry_url = reverse("contact")
        self.form_data= {
            "name": "Shrek",
            "email": "shrek@ogre.com",
            "phone": "0111223344556",
            "message": "Ogres Are Like Onions.",
            "receive_copy": "",
        } 
        
        self.context = {
                    'enquiry': {
                        'name': self.form_data['name'],
                        'email': self.form_data['email'],
                        'phone': self.form_data['phone'],
                        'message': self.form_data['message'],},
                    'subtitle': 'You have received a new enquiry from the website:',
                    'recipient': 'Admin',}

    def test_contact_page_uses_correct_template(self):
        response = self.client.get(reverse("contact"))
        self.assertTemplateUsed(response,'home/contact.html')

    def test_render_enquiry_form_in_contact_page(self):
        response = self.client.get(reverse("contact"))
        self.assertContains(response,'Send Us Your Enquiry', status_code=200)
        self.assertContains( response, "Receive a copy of this enquiry")
        self.assertIsInstance(response.context['form'], UserContactForm)

    @patch('home.views.send_mail')
    def test_send_email_from_contact_page_to_site_admim(self, mock_send_mail):
        
        response = self.client.post(self.contact_enquiry_url, self.form_data)

        # success submission message is shown
        self.assertContains(response, "Thank you for your enquiry!", status_code=200) 

        self.context['subtitle']= 'You have received a new enquiry from the website:'
        self.context['recipient']= 'Admin'
            
        html_message = render_to_string('home/enquiry-email.html', self.context)
        text_message = strip_tags(html_message)        
        # check if send_mail was called once
        mock_send_mail.assert_called_once_with(
            subject='New Website Enquiry from ' + self.form_data['name'],
            message=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL,],
            html_message=html_message,)

    @patch('home.views.send_mail')
    def test_enquiry_copy_email_sent_to_site_visitor_on_valid_form_submission_contact_page(self, mock_send_mail):
        
        #check the receive copy field
        self.form_data["receive_copy"]="checked"
        response = self.client.post(self.contact_enquiry_url, self.form_data)

        # success submission message is shown
        self.assertContains(response, "Thank you for your enquiry!", status_code=200) 
        self.assertEqual(mock_send_mail.call_count, 2) # called twice, 2nd to visitor
