from http import HTTPStatus
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from apps.users.models import User, EmailVerification


# Create your tests here.
class UserRegisterViewTestCase(TestCase):

    def setUp(self):
        self.data = {
            'first_name': 'Valerii', 'last_name': 'Pavlikov',
            'username': 'valerii', 'email': 'valerypavlikov@yandex.ru',
            'password1': '12345678pP', 'password2': '12345678pP',
        }
        self.path = reverse('register')


    def test_user_register_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(response, 'users/register.html')


    def test_user_register_post_success(self):
        response = self.client.post(self.path, self.data)

        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())

        # check creating of user
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        # check creating of email verification
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_registration_post_error(self):
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)