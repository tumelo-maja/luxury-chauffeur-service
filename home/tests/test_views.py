from django.test import SimpleTestCase
from django.shortcuts import reverse
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

    def test_contact_page_uses_correct_template(self):
        response = self.client.get(reverse("contact"))
        self.assertTemplateUsed(response,'home/contact.html')

    def test_render_enquiry_form_in_contact_page(self):
        response = self.client.get(reverse("contact"))
        self.assertContains(response,'Send Us Your Enquiry', status_code=200)
        self.assertContains( response, "Receive a copy of this enquiry")
        self.assertIsInstance(response.context['form'], UserContactForm)
