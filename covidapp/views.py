# Cet fichier gere la vue de notre application, ie les infos que contiennent nos pages html
# ici nous attribuons  les donnees au fichiers html specifique, ces donnees sont alors
# accessible dans les fichiers html.

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Manager, Hospital

# gestion de la connexion ou login
def login(request):
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
    return render(request, 'covidapp/login.html', {'error_message': error_message})


# Gestion du dashboard des managers
def manager_dashboard(request, manager_id):
    # on check si le manager est deja authentifier en regardans les donnees de session
    if 'manager_id' not in request.session or request.session['manager_id'] != manager_id:
        messages.error(request, 'Vous netes pas connecter.')
        return redirect('login')
    # on recuper les infos concernant le manager en utilsant l'id passer lors du login
    manager = Manager.objects.get(id=manager_id)
      
    # ajoutons une gestion de deconnexion
    if request.method == 'POST' and 'signout' in request.POST:
        # Efface les donnees enregistrer dans la session avant de se deconnecter
        request.session.clear()
        return redirect('login')
    # on envoit alors toutes les infos du manager a la page html manager_dashboad
    return render(request, 'covidapp/manager_dashboard.html', {'manager':manager})

# Ajouter un hopital dans notre base de donnee (dans la feille hopital)
def add_hospital(request):
    #On verifie si le manager est authentifier en regardant la session
    if 'manager_id' not in request.session:
        messages.error(request, 'Vous netes pas connecter')
        return redirect('login')
        
    # Recuperer les infos du manager de la session si il est connecte
    manager_id = request.session['manager_id']
    manager = Manager.objects.get(id=manager_id)
    
    if request.method == 'POST':
        # recuperer les donnes de la formulaire hopital
        name = request.POST['name']
        address = request.POST['address']
        
        # Creer un nouvel hopital avec le manager connecter comme createur
        Hospital.objects.create(name=name, address=address, creator=manager)
        
        # Rediriger vers le manager_dashboard
        return redirect('manager_dashboard', manager_id=manager_id)
        
    return render(request, 'covidapp/add_hospital.html', {'manager':manager})
    
    