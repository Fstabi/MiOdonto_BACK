import unittest
from io import StringIO
from unittest.mock import patch
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
from psycopg2 import OperationalError as Psycopg2Error  # type: ignore
from django.db.utils import OperationalError
from django.core.management import call_command


class CustomUserTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.valid_cuit = "20-12345678-9"
        self.invalid_cuit_format = "123-456-789"
        self.invalid_cuit_type = "99-12345678-9"
        self.invalid_cuit_check = "20-12345678-0"

    def test_create_clinic_manager(self):
        """Testa la creazione di un utente con ruolo CLINIC"""
        user = self.User.objects.create_user(
            username="clinic_manager",
            email="manager@clinic.com",
            password="testpass123",
            first_name="Maria",
            last_name="Gomez",
            role="CLINIC",
            cuit=self.valid_cuit,
            phone="1234567890"
        )
        self.assertEqual(user.role, "CLINIC")
        self.assertEqual(user.cuit, self.valid_cuit)
        self.assertEqual(user.get_full_name(), "Maria Gomez")
        self.assertTrue(user.is_clinic_manager)
        self.assertFalse(user.is_dentist)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.email, "manager@clinic.com")  # Email normalizzata

    def test_create_dentist(self):
        """Testa la creazione di un utente con ruolo DENTIST"""
        user = self.User.objects.create_user(
            username="dentist",
            email="dentist@clinic.com",
            password="testpass123",
            first_name="Juan",
            last_name="Perez",
            role="DENTIST",
            specialization="Ortodoncia",
            phone="0987654321"
        )
        self.assertEqual(user.role, "DENTIST")
        self.assertIsNone(user.cuit)
        self.assertEqual(user.specialization, "Ortodoncia")
        self.assertEqual(user.get_full_name(), "Juan Perez")
        self.assertFalse(user.is_clinic_manager)
        self.assertTrue(user.is_dentist)
        self.assertTrue(user.is_active)
        self.assertEqual(user.email, "dentist@clinic.com")  # Email normalizzata

    @unittest.skip("Validators not yet implemented")
    def test_valid_cuit(self):
        """Testa la validazione di un CUIT valido"""
        user = self.User(
            username="testuser",
            email="test@clinic.com",
            password="testpass123",
            role="CLINIC",
            cuit=self.valid_cuit
        )
        user.full_clean()
        user.save()
        self.assertEqual(user.cuit, self.valid_cuit)

    @unittest.skip("Validators not yet implemented")
    def test_invalid_cuit_format(self):
        """Testa un CUIT con formato non valido"""
        user = self.User(
            username="testuser",
            email="test@clinic.com",
            password="testpass123",
            role="CLINIC",
            cuit=self.invalid_cuit_format
        )
        with self.assertRaisesMessage(ValidationError, "El CUIT debe ser en formato"):
            user.full_clean()

    @unittest.skip("Validators not yet implemented")
    def test_invalid_cuit_type(self):
        """Testa un CUIT con tipo di contribuente non valido"""
        user = self.User(
            username="testuser",
            email="test@clinic.com",
            password="testpass123",
            role="CLINIC",
            cuit=self.invalid_cuit_type
        )
        with self.assertRaisesMessage(ValidationError, "El tipo de contribuyente no es válido"):
            user.full_clean()

    @unittest.skip("Validators not yet implemented")
    def test_invalid_cuit_check_digit(self):
        """Testa un CUIT con cifra di controllo non valida"""
        user = self.User(
            username="testuser",
            email="test@clinic.com",
            password="testpass123",
            role="CLINIC",
            cuit=self.invalid_cuit_check
        )
        with self.assertRaisesMessage(ValidationError, "El dígito de control del CUIT no es válido"):
            user.full_clean()

    def test_cuit_unique(self):
        """Testa che il CUIT sia unico"""
        self.User.objects.create_user(
            username="user1",
            email="user1@clinic.com",
            password="testpass123",
            role="CLINIC",
            cuit=self.valid_cuit
        )
        user2 = self.User(
            username="user2",
            email="user2@clinic.com",
            password="testpass123",
            role="CLINIC",
            cuit=self.valid_cuit
        )
        with self.assertRaises(ValidationError):
            user2.full_clean()

    def test_str_representation(self):
        """Testa la rappresentazione stringa dell'utente"""
        user = self.User(
            username="testuser",
            first_name="Ana",
            last_name="Lopez",
            password="testpass123",
            role="DENTIST"
        )
        self.assertEqual(str(user), "Ana Lopez (Odontólogo)")

    def test_created_at_updated_at(self):
        """Testa i campi created_at e updated_at"""
        user = self.User.objects.create_user(
            username="testuser",
            email="test@clinic.com",
            password="testpass123",
            role="CLINIC"
        )
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)
        self.assertLessEqual(user.created_at, timezone.now())
        self.assertLessEqual(user.updated_at, timezone.now())

    def test_email_normalization_lowercase(self):
        """Tests that the email is saved in lowercase"""
        user = self.User.objects.create_user(
            username="testuser",
            email="Test@Clinic.com",
            password="testpass123",
            role="CLINIC"
        )
        self.assertEqual(user.email, "test@clinic.com")

    def test_email_normalization_strip_spaces(self):
        """Tests that spaces in the email are removed"""
        user = self.User.objects.create_user(
            username="testuser",
            email=" test@clinic.com ",
            password="testpass123",
            role="CLINIC"
        )
        self.assertEqual(user.email, "test@clinic.com")

    def test_email_unique_normalized(self):
        """Tests that normalized emails are considered duplicates"""
        self.User.objects.create_user(
            username="user1",
            email="Test@Clinic.com",
            password="testpass123",
            role="CLINIC"
        )
        with self.assertRaises(ValidationError):
            user2 = self.User.objects.create_user(
                username="user2",
                email="test@clinic.com",
                password="testpass123",
                role="CLINIC"
            )
            user2.full_clean()