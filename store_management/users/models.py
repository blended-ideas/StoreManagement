from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, Model, ManyToManyField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class UserRole(Model):
    label = CharField(unique=True, primary_key=True, max_length=50)
    name = CharField(unique=True, max_length=50)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'User Role'
        verbose_name_plural = 'User Roles'


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    roles = ManyToManyField(UserRole, related_name='users')

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
