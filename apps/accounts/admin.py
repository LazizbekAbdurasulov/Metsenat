from django.contrib import admin
from .models import Universities, Student, Sponsor, Sponsorship
# Register your models here.


admin.site.register(Universities)
admin.site.register(Student)
admin.site.register(Sponsor)
admin.site.register(Sponsorship)