from re import T
import re
from statistics import mode
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Universities(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'University'
        verbose_name_plural = 'Universities'


class TYPE_DEGREE(models.TextChoices):
    BACHELOR = 'BACHELOR', 'Bakalavr'
    MAGISTER = 'MAGISTER', 'Magister'

class Student(models.Model):
    first_name = models.CharField(max_length=32, null=False, blank=False)
    last_name = models.CharField(max_length=32, null=False, blank=False)
    university = models.ForeignKey(Universities, on_delete=models.CASCADE)
    degree = models.CharField(max_length=32, choices=TYPE_DEGREE.choices, default=TYPE_DEGREE.BACHELOR, null=False, blank=False)
    course = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    amount = models.IntegerField(null=False, blank=False)
    phone_number = models.IntegerField(null=False, blank=False)
    email = models.EmailField(max_length=48, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        
    
class STATUS_CHOICE(models.TextChoices):
    MODERATION = 'MODERATION', 'Moderatsiya'
    NEW = 'NEW', 'Yangi'
    APPROVED = 'APPROVED', 'Tasdiqlangan'
    CANCELED = 'CANCELED', 'Bekor qilingan'

class TYPE_PERSON(models.TextChoices):
    PHYSICAL = 'PHYSICAL', 'Jismoniy shaxs'
    LEGAL = 'LEGAL', 'Yuridik shaxs'

class Sponsor(models.Model):
    full_name = models.CharField(max_length=256, null=False, blank=False)
    sponsor_type = models.CharField(max_length=32, choices=TYPE_PERSON.choices, default=TYPE_PERSON.LEGAL, null=False, blank=False)
    amount = models.IntegerField(null=False, blank=False)
    status = models.CharField(max_length=32, choices=STATUS_CHOICE.choices, default=STATUS_CHOICE.MODERATION, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    company = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} - {self.amount}"

    class Meta:
        verbose_name = 'Sponsor'
        verbose_name_plural = 'Sponsors'


class Sponsorship(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        student_fullname = f"{self.student.first_name} {self.student.last_name}"
        return f"Sponsor: {self.sponsor.full_name} -> Student: {student_fullname}! Amount: {self.amount}"
    
    class Meta:
        verbose_name = 'Sponsorship'
        verbose_name_plural = 'Sponsorships'