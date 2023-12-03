# Cet fichier gere la vue de notre application, ie les infos que contiennent nos pages html
# ici nous attribuons  les donnees au fichiers html specifique, ces donnees sont alors
# accessible dans les fichiers html.

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Manager, Hospital, Doctor, Patient, User
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

# Page d'accueil
def home(request):
    return render(request, 'covidapp/home.html')

# gestion de la connexion ou login des managers
def manager_login(request):
    error_message = None # montre l'erreur au cas ou l'utilisateur n'existe pas
    #Ici on recuperer les infos ou donnees contenus dans la page login apres
    # que l'utilisateur est cliquer sur envoyer. Donnees qui sont dans la request
    # on check alors si il s'agit de la requette envoie (POST) pour recuperer les donnees
    # et les analysees
    if request.method == 'POST':
        pseudo = request.POST['pseudo']
        password = request.POST['password']
        
        # apres avoir recuperer les donnes et les placees dans nos variables
        # on check si ces donnees existent dans notre table ou feuille Manager
        try:
            manager = Manager.objects.get(pseudo=pseudo, password=password)
            # Si les donnees exist ie le manager exist on ajoute une session et le redirect vers la page
            # manager_dashboard avec les donnees (ici manager_id)
            request.session['manager_id'] = manager.id
            request.session['manager_pseudo' ] = manager.pseudo
            request.session['manager_first_name'] = manager.first_name
            request.session['manager_last_name' ] = manager.last_name
            #redirection au dashboard manager
            return redirect('manager_dashboard', manager_id=manager.id)
        except Manager.DoesNotExist:
            # si le manager n'existe pas, on envoie un message d'erreur
            error_message = 'Pseudo ou password incorrect'
    
    # au cas ou l'utilisateur n'existe pas on renvoir a la page login avec l'erreur
    return render(request, 'covidapp/manager_login.html', {'error_message': error_message})


# Gestion du dashboard des managers
def manager_dashboard(request, manager_id):
    # on check si le manager est deja authentifier en regardans les donnees de session
    if 'manager_id' not in request.session or request.session['manager_id'] != manager_id:
        messages.error(request, 'Vous netes pas connecter.')
        return redirect('manager_login')
    # on recuper les infos concernant le manager en utilsant l'id passer lors du login
    manager = Manager.objects.get(id=manager_id)
      
    # ajoutons une gestion de deconnexion
    if request.method == 'POST' and 'signout' in request.POST:
        # Efface les donnees enregistrer dans la session avant de se deconnecter
        request.session.clear()
        return redirect('manager_login')
    # on envoit alors toutes les infos du manager a la page html manager_dashboad
    return render(request, 'covidapp/manager_dashboard.html', {'manager':manager})

# Ajouter un hopital dans notre base de donnee (dans la feille hopital)
def add_hospital(request):
    #On verifie si le manager est authentifier en regardant la session
    if 'manager_id' not in request.session:
        messages.error(request, 'Vous netes pas connecter')
        return redirect('manager_login')
        
    # Recuperer les infos du manager de la session si il est connecte
    manager_id = request.session['manager_id']
    manager = Manager.objects.get(id=manager_id)
    
    # Recuperer la list des hopitaux en le rageant par date et le derniers dajouter comme le premier
    # ces donnees seront aussi envoyer a la page pour afficher la liste des hopitaux dans la BD
    hospitals = Hospital.objects.order_by('-id')
    
    if request.method == 'POST':
        # recuperer les donnes de la formulaire hopital
        name = request.POST['name']
        address = request.POST['address']
        
        # Creer un nouvel hopital avec le manager connecter comme createur
        Hospital.objects.create(name=name, address=address, creator=manager)
        
        # Rediriger vers la meme page avec la liste d'hopitaux mise a jour 
        return redirect('add_hospital')
        
    return render(request, 'covidapp/add_hospital.html', {'manager':manager, 'hospitals': hospitals})
    
# Ajouter un docteur/ un medecin dans notre base de donne
def add_doctor(request):
    # Verifie si le manager est connecter avec les donnee dans la session
    # Si il y'a aucune connexion on renvoie vers le login du manager
    if 'manager_id' not in request.session:
        messages.error(request, 'Vous netes pas connectee')
        return redirect('manager_login')
    
    # Recuperer les infos du manager
    manager_id = request.session['manager_id']
    manager = Manager.objects.get(id=manager_id)
    
    # Recuperer les infos des hopitaux
    hospitals = Hospital.objects.order_by('name')
    
    # Recuperer les donnees dans le formulaire
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        creator_id = request.POST['creator']
        hospital_id = request.POST['hospital']

        # Creer ou enregistrer dans la base de donnee
        Doctor.objects.create(
            full_name=full_name,
            email=email,
            password=password,
            address=address,
            creator_id=creator_id,
            hospital_id=hospital_id
        )
        
        # Notification d'envoie
        messages.success(request, 'docteur ajouter. ')
        
        # Redirige vers la page add_doctor
        return redirect('add_doctor')
    
    # envoie les donnees au fichier add_doctor.html
    return render(request, 'covidapp/add_doctor.html', {'manager': manager, 'hospitals':hospitals})

# Creons le login pour le docteur
def doctor_login(request):
    # On recupere les donnees ou elements envoie depuis le formulaire login docteur
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        #On essaie de voir si il existe dans la BD un docteur a qui ces elements correspondent
        try:
            doctor = Doctor.objects.get(email=email, password=password)
        except Doctor.DoesNotExist:
            # Si les elements ne correspondent a personne on renvoie a la page login avec
            # une notification d'erreur
            message.error(request, 'Email ou mot de passe incorrect')
            return redirect('doctor_login')
            
        # Si les elements correspondent a ceux d'un docteur dans la BD, on cree une session
        # pour cet utilisateur et on l'envoie a la page doctor_dashboad
        request.session['doctor_id'] = doctor.id
        return redirect('doctor_dashboard')
        
    return render(request, 'covidapp/doctor_login.html')


# Gestion du dashboard doctor
def doctor_dashboard(request):
    # verifier si le docteur est bien authentifier
    if 'doctor_id' not in request.session:
        messages.error(request, 'Veuillez vous connecter')
        return redirect('doctor_login')
    
    # Recuperer les infos sur le medecin    
    doctor_id = request.session['doctor_id']
    doctor = Doctor.objects.get(id=doctor_id)
    
    # recuperer la liste des patient du docteur
    patients = Patient.objects.filter(doctor=doctor)
    
    return render(request, 'covidapp/doctor_dashboard.html', {'doctor':doctor, 'patients':patients})

# Gestion de la deconnexion de docteur
def doctor_signout(request):
    # Verifie si le doctor est authentifier dans les donnees session
    if 'doctor_id' in request.session:
        # Deconnecter le docteur
        del request.session['doctor_id']
        
    return redirect('doctor_login')

# Ajouter un patient
def add_patient(request):
    # Check if doctor is authenticated by checking session data
    if 'doctor_id' not in request.session:
        messages.error(request, 'You are not authenticated. Please log in.')
        return redirect('doctor_login')

    # Retrieve doctor information from session data
    doctor_id = request.session['doctor_id']
    doctor = Doctor.objects.get(id=doctor_id)

    # Retrieve hospital information from doctor's associated hospital
    hospital = doctor.hospital

    if request.method == 'POST':
        # Process the form data when submitted
        full_name = request.POST['full_name']
        address = request.POST['address']
        symptoms = request.POST['symptoms']
        medications = request.POST['medications']
        status = request.POST['status']
        disease_history = request.POST['disease_history']
        contact_number = request.POST['contact_number']

        # Create a new patient record in the database
        patient = Patient.objects.create(
            full_name=full_name,
            address=address,
            symptoms=symptoms,
            medications=medications,
            status=status,
            disease_history=disease_history,
            contact_number=contact_number,
            hospital=hospital,
            doctor=doctor
        )

        messages.success(request, 'Patient successfully added.')
        return redirect('doctor_dashboard')

    return render(request, 'covidapp/add_patient.html', {'doctor': doctor, 'hospital': hospital})

# Pour afficher la liste complete des patients
def patient_list(request):
    # Check if doctor is authenticated by checking session data
    if 'doctor_id' not in request.session:
        messages.error(request, 'You are not authenticated. Please log in.')
        return redirect('doctor_login')

    # Retrieve doctor information from session data
    doctor_id = request.session['doctor_id']
    doctor = Doctor.objects.get(id=doctor_id)
    hospital = doctor.hospital

    # Retrieve all patients associated with the doctor
    patients = Patient.objects.filter(hospital=hospital)

    return render(request, 'covidapp/patient_list.html', {'hospital': hospital, 'doctor': doctor, 'patients': patients})
    

# cette function gere l'enregistrement des nouveax utilisateurs
def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # on verifie si l'email ecrit existe deja dans notre BD
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, 'covidapp/user_registration.html', {'form': form, 'error': 'Email existe deja, veuillez le changer'})
            
            # on verifier si le password sont correct
            if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
                return render(request, 'covidapp/user_registration.html', {'form': form, 'error':'le password ne correspondent pas.'})
            
            # Si tout va bien, On cree un nouveau utilisateur
            user = form.save()
            # On redirige l'utilisateur a la page user login
            messages.success(request, 'Vous enregistez avec succee, veuillez aller a login pour vous connectez')
            # Redirect a login
            return redirect('user_login')
    else:
        form = UserRegistrationForm()
    
    # L'Etat initial du formulaire sans erreur
    return render(request, 'covidapp/user_registration.html', {'form':form, 'error': None})

# Cree la page user login
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Authenticate user
            user = authenticate(request, email=email, password=password)

            if user is not None:
                # Login the user
                login(request, user)
                # Redirect to the user dashboard page
                return redirect('user_dash')
            else:
                # Display error message
                messages.error(request, 'Invalid email or password.')

    else:
        form = UserLoginForm()

    return render(request, 'covidapp/user_login.html', {'form': form})

# gestion du user dashboard
def user_dash(request):
    return render(request, 'covidapp/user_dash.html')