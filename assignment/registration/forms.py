from django.forms import ModelForm, fields
from .models import User


class UserRegistrationForm(ModelForm):
    password = fields.CharField(max_length=288, required=True)

    class Meta:
        model = User
        exclude = ['is_staff', 'is_superuser' , 'user_id']