from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken

class UserViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.access_token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_get_user(self):
        """
        Test retrieving the authenticated user's data.
        """
        response = self.client.get(reverse('user-list'))  # Assuming 'user-list' is the URL name for 'UserViewSet'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['id'], self.user.id)

class RegisterTests(APITestCase):
    def test_register_user(self):
        """
        Test registering a new user.
        """
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword",
            "first_name": "New",
            "last_name": "User"
        }
        response = self.client.post(reverse('register-list'), data, format='json')  # Assuming 'register-list' is the URL name for 'Register'
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 2)  # Check that a new user has been created

class ReferralListTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.access_token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_get_referral_list(self):
        """
        Test retrieving the list of users referred by the authenticated user.
        """
        response = self.client.get(reverse('referrals-list'))  # Assuming 'referrals-list' is the URL name for 'ReferralList'
        self.assertEqual(response.status_code, 200)
        # You can add more assertions here to check the returned data if needed
