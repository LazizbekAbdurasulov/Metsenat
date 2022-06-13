from asyncore import read
from rest_framework import serializers
from .validators import validate_amount
from .models import Universities, Student, Sponsor, Sponsorship
from django.db.models.functions import Coalesce
from django.db.models import Sum, Count
from .services import create_sponsorship, update_sponsorship


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Universities
        fields = '__all__'
    
class SponsorSerializer(serializers.ModelSerializer):
    used_money = serializers.SerializerMethodField()

    class Meta:
        model = Sponsor
        fields = ['id', 'full_name', 'amount', 'used_money', 'status', 'sponsor_type', 'company',  'created_date']
        extra_kwargs = {
            'money': {'allow_null': False, 'required': True, 'validators':[validate_amount]},
        }

    def create(self, validate_data):
        validate_data['status'] = 'MODERATION'
        sponsor = Sponsor.objects.create(**validate_data)
        return sponsor

    @staticmethod
    def get_used_money(sponsor):
        used_money = Sponsorship.objects.filter(sponsor_id=sponsor.id).aggregate(money=Coalesce(Sum('amount'), 0))['money']
        return used_money

    def get_company_name(self, name):
        if self.initial_data.get('sponsor_type') == "LEGAL":
            return name
        else:
            return None

class StudentSerializer(serializers.ModelSerializer):
    university = UniversitySerializer(read_only=True)
    university_id = serializers.IntegerField(allow_null=False, required=True, write_only=True)
    gained_amount = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'degree', 'course', 'amount', 'university', 'gained_amount', 'university_id']
        
        extra_kwargs = {
            'amount_error': {'allow_null': False, 'required':True, 'validators': [validate_amount]}
        }
    
    @staticmethod
    def get_gained_amount(student):
        gained_amount = Sponsorship.objects.filter(student_id=student.id).aggregate(money=Coalesce(Sum('amount'), 0))['money']
        print(student.id)
        return gained_amount
    

class SponsorshipSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    sponsor = SponsorSerializer(read_only=True)

    student_id = serializers.IntegerField(allow_null=False, required=True, write_only=True)
    sponsor_id = serializers.IntegerField(allow_null=False, required=True, write_only=True)
    class Meta:
        model = Sponsorship
        fields = ['id', 'sponsor', 'student', 'id', 'sponsor_id', 'student_id', 'amount']
        extra_kwargs = {
            'amount_error': {'allow_null': False, 'required':True, 'validators': [validate_amount]}
        }
    
    def create(self, validated_data):
        data = create_sponsorship(validated_data=validated_data)
        return data
    
    def update(self, instance, validated_data):
        instance = update_sponsorship(instance, validated_data)
        return instance    
