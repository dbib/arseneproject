# Cet fichier gere la vue de notre application, ie les infos que contiennent nos pages html
# ici nous attribuons  les donnees au fichiers html specifique, ces donnees sont alors
# accessible dans les fichiers html.

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Manager, Hospital, Doctor, Patient, User, Attente
from .forms import UserRegistrationForm
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
            messages.error(request, 'Email ou mot de passe incorrect')
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
    
    # Recuperer la liste d'attente
    users_in_attente = Attente.objects.filter(hospital = doctor.hospital.id)
    
    return render(request, 'covidapp/doctor_dashboard.html', {'doctor':doctor, 'patients':patients, 'users_in_attente': users_in_attente})

# Gestion de la deconnexion de docteur
def doctor_signout(request):
    # Verifie si le doctor est authentifier dans les donnees session
    if 'doctor_id' in request.session:
        # Deconnecter le docteur
        del request.session['doctor_id']
        
    return redirect('doctor_login')

# Ajouter un patient
def add_patient(request):
    # Verifier si le docteur est authentifier pour ajouter un patient
    if 'doctor_id' not in request.session:
        messages.error(request, 'You are not authenticated. Please log in.')
        return redirect('doctor_login')

    # Recuperer les donnees du serveur
    doctor_id = request.session['doctor_id']
    doctor = Doctor.objects.get(id=doctor_id)

    # Recuperer le nom de l'hopital ou le docteur exerce
    hospital = doctor.hospital

    if request.method == 'POST':
        # Recuperer les donnes du formulaire
        full_name = request.POST['full_name']
        birth_date = request.POST['birth_date']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        symptoms = request.POST['symptoms']
        medications = request.POST['medications']
        status = request.POST['status']
        disease_history = request.POST['disease_history']

        # Creer ou ajouter un nouveau patient dans la base des donnees
        patient = Patient.objects.create(
            full_name=full_name,
            birth_date=birth_date,
            email=email,
            phone=phone,
            address=address,
            symptoms=symptoms,
            medications=medications,
            status=status,
            disease_history=disease_history,
            hospital=hospital,
            doctor=doctor
        )

        messages.success(request, 'Patient successfully added.')
        return redirect('doctor_dashboard')
    
    # Si le patient est selectionner depuis la liste d'attente
    attente_id = request.GET.get('attente_id')
    if attente_id:
        try:
            #Recuperer les donnes de la liste d'attente
            attente_user = Attente.objects.get(id=attente_id)
        except Attente.DoesNotExist:
            messages.error(request, 'Le patient nest pas disponible')
            return redirect('doctor_dashboard')
        
        # Completer certaines parties du formulaire add patient
        initial_data = {
            'full_name': attente_user.full_name,
            'email': attente_user.email,
            'phone': attente_user.phone,
            'address': '',
            'symptoms': '',
            'medications': '',
            'status': '',
            'disease_history': '',
        }
        
        # Passer les donner initial au formulaire
        return render(request, 'covidapp/add_patient.html', {'doctor': doctor, 'hospital': hospital, 'initial_data': initial_data})
    else:
        # Creer un formulaire vide
        return render(request, 'covidapp/add_patient.html', {'doctor': doctor, 'hospital': hospital, 'initial_data': None})

    return render(request, 'covidapp/add_patient.html', {'doctor': doctor, 'hospital': hospital, 'initial_data': None})

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
    # recuperation des donnee envoyer depuis le formulaire
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Check pour voir si il y a une correspondance dans la BD
        try:
            user = User.objects.get(email=email, password=password)
        except User.DoesNotExist:
            # si il n'ya aucune correspondance
            messages.error(request, 'Email ou mot de passe incorrect')
            return redirect('user_login')
        
        # s'il y a bel et bien correspondance
        # On cree une session pour le user
        request.session['user_id'] = user.id
        return redirect('user_dashboard')
    
    return render(request, 'covidapp/user_login.html')
# gestion du user dashboard
def user_dashboard(request):
    # verifier si le user est authentifier
    if 'user_id' not in request.session:
        messages.error(request, "Veuillez vous connect")
        return redirect('user_login')
    
    # Recuper les infos du user si il est authentifier
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    
    # Rechercher les donnes relatives a l'historique du user dans la table patient
    user_patients = Patient.objects.filter(email=user.email)
    
    # Afficher la page user dashboard
    return render(request, 'covidapp/user_dashboard.html', {'user':user, 'user_patients': user_patients})

# La deconnexion de l'utilisateur
def user_logout(request):
    #verifier si le user est authentifier dans la BD
    if 'user_id' in request.session:
        # deconnecter
        del request.session['user_id']
        
    return redirect('user_login')

# S'ajouter a la liste d'attente ou demande une consultation
def ask_consultation(request):
    # verifier si l'utilisateur est authentifier
    if 'user_id' not in request.session:
        messages.error(request, "Vous n'etes pas connecté, veuillez vous connecter")
        return redirect('user_login')
        
    # Recuperer les donnees dont nous auront besoin dans notre formulaire
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    
    hospitals = Hospital.objects.order_by('name')
    
    # Envoie des donnees dans le model Attente
    if request.method == 'POST':
        # recuperer les donnees du formulaire
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone = request.POST['phone']
        hospital_id = request.POST['hospital']
        
        # Ajouter dans la liste d'attente
        Attente.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            hospital_id=hospital_id
        )
        
        # Notification d'envoie
        messages.success(request, "vous avez été ajouté à la liste dattente")
    
        # Rediriger au user_dashboard
        return redirect('user_dashboard')
    
    return render(request, 'covidapp/ask_consultation.html', {'user': user, 'hospitals':hospitals})