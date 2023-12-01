from django.contrib import admin
from .models import Manager, Hospital, Doctor, Patient

admin.site.register(Manager)
admin.site.register(Hospital)
admin.site.register(Doctor)
admin.site.register(Patient)
# Register your models here.
