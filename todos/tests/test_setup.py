from random import randrange

from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.urls import reverse

class TodoSetup():
    API_CLIENT = None
    USER = None
    RESPONSE = None

    def __init__(self):
        self.create_api_client()
        self.create_user()
        self.auth_user()

    def create_api_client(self):
        self.API_CLIENT = APIClient()
    
    def create_user(self):
        self.USER = {
            'username': f'testUser{randrange(50) + randrange(5)}',
            'password': '321ewq321'
        }
        new_user = User.objects.create(username=self.USER['username'])
        new_user.is_active = True
        new_user.set_password(self.USER['password'])
        new_user.save()

    def auth_user(self):
        tokens = self.get_token_for_user(self.USER)
        formated_token = self.get_formatted_token(tokens)
        self.API_CLIENT.credentials(HTTP_AUTHORIZATION=formated_token)

    def get_token_for_user(self, user):
        login_url = reverse('loginUser')
        res = self.API_CLIENT.post(login_url, user, format='json')
        return res.data

    def get_formatted_token(self, tokens):
        return f'Bearer {tokens["access"]}'

    # Request
    def do_get(self, url, return_data=True):
        self.RESPONSE = self.API_CLIENT.get(url)
        if return_data:
            return self.RESPONSE.data
        else:
            self.RESPONSE
    
    def do_post(self, url, payload=None):
        self.RESPONSE = self.API_CLIENT.post(url, payload, format='json')
        return self.RESPONSE
    def do_put(self, url, payload=None):
        self.RESPONSE = self.API_CLIENT.put(url, payload, format='json')
        return self.RESPONSE
    def do_patch(self, url, payload=None):
        self.RESPONSE = self.API_CLIENT.patch(url, payload, format='json')
        return self.RESPONSE

    def do_delete(self, url):
        self.RESPONSE = self.API_CLIENT.delete(url)
        return self.RESPONSE
