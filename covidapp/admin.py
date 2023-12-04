from django.contrib import admin
from .models import Manager, Hospital, Doctor, Patient, User, Attente

admin.site.register(Manager)
admin.site.register(Hospital)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(User)
admin.site.register(Attente)
# Register your models here.
