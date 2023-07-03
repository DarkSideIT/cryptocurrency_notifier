import unittest


from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse


User = get_user_model()


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
            register_time=timezone.now(),
            balance=0,
            chosen_coins=["coin1", "coin2"],
            access_level="user"
        )

    def test_user_creation(self):
        self.assertIsInstance(self.user, User)
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertTrue(self.user.check_password("testpassword"))
        self.assertEqual(self.user.register_time.date(), timezone.now().date())
        self.assertEqual(self.user.balance, 0)
        self.assertEqual(self.user.chosen_coins, ["coin1", "coin2"])
        self.assertEqual(self.user.access_level, "user")

    def test_user_authentication(self):
        authenticated_user = User.objects.authenticate(username="testuser", password="testpassword")
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user, self.user)

    def test_user_str_representation(self):
        self.assertEqual(str(self.user), "testuser")
        

class RegistrationTestCase(TestCase):
    def test_registration_form(self):
        url = reverse("register/")
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "testpassword",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Проверка успешного перенаправления
        self.assertEqual(User.objects.count(), 1)  # Проверка создания нового пользователя

        user = User.objects.get(username="testuser")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.check_password("testpassword"))

    def test_registration_form_invalid_data(self):
        url = reverse("register/")
        data = {
            "username": "testuser",
            "email": "invalid_email",  # Некорректный формат email
            "password1": "testpassword",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # Проверка кода ответа, который означает ошибку валидации формы
        self.assertEqual(User.objects.count(), 0)  # Проверка, что пользователь не был создан

        error_messages = response.context["form"].errors  # Получение сообщений об ошибках из контекста ответа
        self.assertIn("email", error_messages)  # Проверка наличия ошибки для поля email
        self.assertIn("password2", error_messages)
