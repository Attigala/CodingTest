from django.test import TestCase, Client
from django.urls import reverse, resolve

from django.contrib.auth.models import User


from .views import home, team
# Create your tests here.
class HomeTest(TestCase):

    def test_home_unauthentcated(self):
        url = reverse('home')
        response=self.client.get(url)
        self.assertEquals(response.status_code,403)
    
    def test_home_authenticated(self):
        url=reverse('home')

        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        self.client= Client()
        logged_in=self.client.login(username="testuser", password="12345")
        response=self.client.get(url)
        self.assertEquals(response.status_code,200)