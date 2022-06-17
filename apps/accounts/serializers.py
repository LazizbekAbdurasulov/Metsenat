from dataclasses import dataclass
from itertools import count
from rest_framework import serializers
from django.db.models.functions import Coalesce
from django.db.models import Sum, Count

from .services import create_sponsorship, update_sponsorship
from .validators import validate_amount, phone_number, full_name
from .models import Universities, Student, Sponsor, Sponsorship


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Universities
        fields = '__all__'


class SponsorSerializer(serializers.ModelSerializer):
    used_money = serializers.SerializerMethodField()
    class Meta:
        model = Sponsor
        fields = [
            'id', 'full_name', 'phone_number', 'amount', 'used_money', 'status',
            'sponsor_type', 'company',  'created_date',
            ]
        extra_kwargs = {
            'amount': {'allow_null': False, 'required': True, 'validators': [validate_amount]},
            'phone_number': {'allow_null': False, 'required': True, 'validators': [phone_number]},
            'full_name': {'allow_null': False, 'required': True, 'validators': [full_name]}
            
        }

    def create(self, validate_data):
        validate_data['status'] = 'MODERATION'
        sponsor = Sponsor.objects.create(**validate_data)
        return sponsor

    @staticmethod
    def get_used_money(sponsor):
        used_money = Sponsorship.objects.filter(sponsor_id=sponsor.id).aggregate(money=Coalesce(Sum('amount'), 0))['money']
        return used_money




class StudentSerializer(serializers.ModelSerializer):
    university = UniversitySerializer(read_only=True)
    university_id = serializers.IntegerField(allow_null=False, required=True, write_only=True)
    gained_amount = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = [
            'id', 'first_name', 'last_name', 'phone_number', 'degree',
             'amount', 'university', 'gained_amount', 'university_id'
            ]
        extra_kwargs = {
            'amount': {'allow_null': False, 'required':True, 'validators': [validate_amount]}
        }
    
    @staticmethod
    def get_gained_amount(student):
        gained_amount = Sponsorship.objects.filter(student_id=student.id).aggregate(money=Coalesce(Sum('amount'), 0))['money']
        return gained_amount


class SponsorshipSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    sponsor = SponsorSerializer(read_only=True)

    student_id = serializers.IntegerField(allow_null=False, required=True, write_only=True)
    sponsor_id = serializers.IntegerField(allow_null=False, required=True, write_only=True)

    class Meta:
        model = Sponsorship
        fields = [
            'id', 'sponsor', 'student', 'id', 'sponsor_id',
            'student_id', 'amount'
            ]
        extra_kwargs = {
            'amount': {'allow_null': False, 'required':True, 'validators': [validate_amount]}
        }
    
    def create(self, validated_data):
        data = create_sponsorship(validated_data=validated_data)
        return data
    
    def update(self, instance, validated_data):
        instance = update_sponsorship(instance, validated_data)
        return instance




class DashboardSerializer:
    def __init__(self):
        self.paid_money = Sponsorship.objects.aggregate(Sum('amount'))['amount__sum']
        if self.paid_money is None:
            self.paid_money = 0
        self.requested_money = Student.objects.aggregate(Sum('amount'))['amount__sum']
        if self.requested_money is None:
            self.requested_money = 0
        self.to_be_paid = self.requested_money - self.paid_money

    @property
    def data(self):
        return self.__dict__


class StatDashboardSerializer:
    def __init__(self):
        self.sponsors_stats = Sponsor.objects.extra({'created_date': "date(created_date)"}).values(
            'created_date').annotate(
            count=Count('id')).values_list('created_date', 'count')
        self.students_stats = Student.objects.extra({'created_date': "date(created_date)"}).values(
            'created_date').annotate(
            count=Count('id')).values_list('created_date', 'count')

    @property
    def data(self):
        return self.__dict__