# covidapp/forms.py
from django import forms
from .models import Doctor, Hospital, Patient, User


# Formulaire pour ajouter un docteur
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['full_name', 'email', 'password', 'address', 'hospital', 'creator']

    def __init__(self, *args, **kwargs):
        # Recuperer les informations du manager avec kwargs
        manager = kwargs.pop('manager', None)

        super().__init__(*args, **kwargs)

        # remplir automatiquement la place creator avec les infos du manager
        if manager:
            self.initial['creator'] = manager.id

        # Cacher creator du formulaire
        self.fields['creator'].widget = forms.HiddenInput()
        
        # Offrir les choix automatique entre les hopitaux dans la BD
        self.fields['hospital'].queryset = Hospital.objects.all()

# Formulaire pour ajouter un Hopital
class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['name', 'address']

# Formulaire pour ajouter un patient
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['full_name', 'address', 'symptoms', 'medications', 'status', 'disease_history', 'contact_number', 'hospital', 'doctor']


# Formulaire pour ajouter un utilisateur
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'password']
