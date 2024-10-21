from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
import re


def validate_password(value):
    """
    Validates that the password contains at least:
    - One uppercase letter
    - One lowercase letter
    - One digit
    - One special character
    """
    if (not re.search(r'[A-Z]', value) or       # At least one uppercase letter
        not re.search(r'[a-z]', value) or       # At least one lowercase letter
        not re.search(r'\d', value) or          # At least one digit
        not re.search(r'[!@#$%^&*(),.?":{}|<>]', value)): # At least one special character
        raise ValidationError(
            "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character."
        )


def validate_age(value):
    """
    Validates that the user is at least 18 years old.
    """
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError("You must be at least 18 years old.")


# Create your models here.
class CustomUser(models.Model):
    name = models.CharField(max_length=30)
    phone = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=128, validators=[validate_password])
    date_of_birth = models.DateField(validators=[validate_age])
