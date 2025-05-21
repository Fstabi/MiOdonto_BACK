from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Custom user model that extends AbstractUser.
    Adds fields specific to the dental clinic management system.
    """
    ROLE_CLINIC = 'CLINIC'
    ROLE_DENTIST = 'DENTIST'
    ROLE_CHOICES = (
        (ROLE_CLINIC, _('Gestor de Clínica')),
        (ROLE_DENTIST, _('Odontólogo')),
    )

    email = models.EmailField(
        _('Correo electrónico'),
        unique=True,
        blank=False,
        error_messages={
            'unique': _('Ya existe un usuario con este correo electrónico.'),
        }
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_CLINIC,
        verbose_name=_('Rol')
    )
    cuit = models.CharField(
        max_length=14,
        unique=True,
        blank=True,
        null=True,
        #validators=[validate_cuit_format, validate_cuit],
        verbose_name=_('CUIT')
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        verbose_name=_('Teléfono')
    )
    specialization = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Especialización')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creado en')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Actualizado en')
    )

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    @property
    def is_clinic_manager(self):
        return self.role == self.ROLE_CLINIC

    @property
    def is_dentist(self):
        return self.role == self.ROLE_DENTIST

    def save(self, *args, **kwargs):
        """Normalize email before saving."""
        if self.email:
            self.email = self.email.strip().lower()
        super().save(*args, **kwargs)