from django.contrib import admin
from .models import Manager, Hospital, Doctor, Patient, User

admin.site.register(Manager)
admin.site.register(Hospital)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(User)
# Register your models here.
