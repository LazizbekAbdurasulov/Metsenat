from rest_framework.validators import ValidationError

def validate_amount(number):
    if number > 0:
        return number
    else:
        raise ValidationError("Pul miqdorini kiritishda xatolik!")

def phone_number(number):
    if len(str(number)) == 12 and str(number)[0:3] == "998":
        return number
    else:
        raise ValidationError("Telefon raqam noto'g'ri kiritildi!")

def full_name(name):
    if len(name.split(' ')) > 1:
        return name
    else:
        raise ValidationError("Ism-sharifingiz to'liq emas!")
