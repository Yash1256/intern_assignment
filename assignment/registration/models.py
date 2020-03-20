from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from .manager import UserManager
from django.db.models import signals
from django.dispatch import receiver
import random


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="Author Email", unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    user_id = models.CharField(max_length=25, blank=True, null=True)
    name = models.CharField(max_length=228)
    phone_no = models.CharField(unique=True, validators=[], max_length=10)
    Role = models.CharField(max_length=100, default='Guest')
    Status = models.CharField(max_length=100, default='Active')

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    objects = UserManager()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def has_perm(self, perm, obj=None):
        return self.is_superuser and self.is_staff

    def has_perms(self, perm_list, obj=None):
        return self.is_superuser and self.is_staff

    def has_module_perms(self, module):
        return self.is_superuser and self.is_staff


def generate_random_string(length=25):
    choices = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    selected_arr = [random.choice(choices) for _ in range(length)]

    rand_string = "".join(selected_arr)

    return rand_string


def generate_public_id(object, length=25):
    rand_string = generate_random_string(length)

    while object.__class__.objects.filter(user_id=rand_string).exists():
        rand_string = generate_random_string()

    return rand_string


@receiver(signals.post_save, sender=User)
def user_id_creation(sender, instance, created=False, **kwargs):
    if created:
        instance.user_id = generate_public_id(instance, 25)
        instance.save()
