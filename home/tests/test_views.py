from django.test import TestCase, SimpleTestCase
from django.shortcuts import reverse

class TestHomeViews(SimpleTestCase):

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

               