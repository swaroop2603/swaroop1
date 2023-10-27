from rest_framework.test import APITestCase
from django.urls import reverse
from .models import User
class TestSetup(APITestCase):
    def setUp(self):
        self.signin_url = reverse('signin')
        self.login_url=reverse('login')
        self.token=reverse('token')
        self.logout_url=reverse('logout')
        user_data = {
            'email': "test@gmail.com",
            'username': 'testname',
            'password': 'testpass',
        }


        self.user_data = user_data
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_user_signin(self):
        response = self.client.post(self.signin_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 201)
    def test_user_login_unverified_user(self):
        res=self.client.post(self.login_url,self.user_data,format='json')
        self.assertEqual(res.status_code,405)

    def test_login_verified(self):
        res = self.client.post(self.signin_url, self.user_data, format='json')
        res = self.client.post(self.token, self.user_data, format='json')

        token = res.data.get('jwt')
        res = self.client.get(self.login_url, format='json', **{'HTTP_COOKIE': f'jwt={token}'})
        self.assertEqual(res.status_code, 200)
    def test_logout_verified(self):
        res = self.client.post(self.signin_url, self.user_data, format='json')
        res = self.client.post(self.token, self.user_data, format='json')
        token = res.data.get('jwt')
        res = self.client.post(self.token, self.user_data, format='json')
        self.assertEqual(res.status_code, 200)


