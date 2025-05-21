from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
#from .validators import validate_cuit, validate_cuit_format


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('CLINIC', 'Gestor de Clínica'),  # Nome in spagnolo per l'utente finale
        ('DENTIST', 'Odontólogo'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        verbose_name=_('Rol')  # Etichetta in spagnolo per l'interfaccia
    )
    cuit = models.CharField(
        max_length=14,  # Per formato XX-XXXXXXXX-Y
        unique=True,
        blank=True,
        null=True,
        #validators=[validate_cuit_format, validate_cuit],
        verbose_name=_('CUIT')
    )
    specialization = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Especialización')  # Per dentisti
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Teléfono')
    )
    # clinic_managed = models.ForeignKey(
    #     'Clinic', on_delete=models.SET_NULL, null=True, blank=True, related_name='managers'
    # )  # TODO: Aggiungere questa ForeignKey a Clinic quando sarà creato il modello Clinic
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creado el')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Actualizado el')
    )

    class Meta:
        indexes = [
            models.Index(fields=['cuit']),
            models.Index(fields=['role']),
        ]
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    @property
    def is_clinic_manager(self):
        return self.role == 'CLINIC'

    @property
    def is_dentist(self):
        return self.role == 'DENTIST'

    def save(self, *args, **kwargs):
        # TODO: Aggiungere validazione per clinic_managed quando la ForeignKey sarà inclusa
        # if self.role == 'DENTIST' and self.clinic_managed:
        #     self.clinic_managed = None
        super().save(*args, **kwargs)