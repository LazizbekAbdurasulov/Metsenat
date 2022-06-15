
from .models import Universities, Student, Sponsor, Sponsorship
from django.db.models import Sum
from django.db.models.functions import Coalesce
from rest_framework.generics import get_object_or_404
from rest_framework.validators import ValidationError

def update_sponsorship(data, validate_data):
    student = get_object_or_404(Student, id=validate_data["student_id"])
    sponsor = get_object_or_404(Sponsor, id=validate_data["sponsor_id"])
    money = validate_data["amount"]

    student_money = Sponsorship.objects.filter(student_id=student.id).aggregate(money=Coalesce(Sum('amount'), 0))['money']
    sponsor_money = Sponsorship.objects.filter(sponsor_id=sponsor.id).aggregate(money=Coalesce(Sum('amount'), 0))['money']
    given_money = sponsor_money - sponsor.money

    if money <= given_money:
        if student_money + money <= student.amount:
            data.money = money
            data.sponsor = sponsor
            data.save()
            return data
        else:
            raise ValidationError({'amount_error': "Homiylik puli kontrakt pulidan oshib ketdi."})
    else:
        raise ValidationError({'amount_error': "Afsuski ushbu homiy hisobida yetarlicha mablag' mavjud emas."})



def create_sponsorship(validated_data):
    student = get_object_or_404(Student, id=validated_data["student_id"])
    sponsor = get_object_or_404(Sponsor, id=validated_data["sponsor_id"])
    money = validated_data["amount"]
    print("1", money)

    student_money = Sponsorship.objects.filter(student_id=student.id).aggregate(money=Coalesce(Sum('amount'), 0))['money']
    sponsor_money = Sponsorship.objects.filter(sponsor_id=sponsor.id).aggregate(money=Coalesce(Sum('amount'), 0))['money']
    given_money = sponsor.amount - sponsor_money
    print("given", given_money)
    if money <= given_money:
        if student_money + money <= student.amount:
            sponsorship = Sponsorship.objects.create(**validated_data)
            return sponsorship
        else:
            raise ValidationError({'amount_error': "Homiylik summasi kontrakt summasidan oshib ketdi."})
    else:
        raise ValidationError({'amount_error': "Afsuski ushbu homiy hisobida yetarlicha mablag' mavjud emas."})