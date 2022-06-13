from rest_framework.validators import ValidationError
from rest_framework.generics import get_object_or_404

def validate_amount(number):
    if number > 0:
        return number
    else:
        return ValidationError("Pul miqdorini kiritishda xatolik!")
