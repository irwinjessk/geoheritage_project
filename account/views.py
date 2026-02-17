from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .models import User, Role
from django import forms


def login_view(request):
    """Vue de connexion utilisateur"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Tentative connexion: username={username}, password={password}")
        
        user = authenticate(request, username=username, password=password)
        print(f"Résultat authentification: {user}")
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue {user.username} !')
            print("Redirection vers heritage:list")
            return redirect('heritage:list')
        else:
            messages.error(request, 'Identifiants invalides')
            print("Identifiants invalides")
    
    return render(request, 'account/login.html')


def logout_view(request):
    """Vue de déconnexion"""
    logout(request)
    messages.info(request, 'Vous êtes déconnecté')
    return redirect('account:login')


# Formulaire personnalisé pour l'inscription avec email
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Adresse email requise')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

def register_view(request):
    """Vue d'inscription"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Récupérer le rôle choisi (par défaut: utilisateur)
            role_name = request.POST.get('role', 'utilisateur')
            user_role = Role.objects.get(name=role_name)
            user.roles.add(user_role)
            
            login(request, user)
            messages.success(request, f'Compte créé pour {user.username} avec le rôle {user_role.name} !')
            return redirect('heritage:list')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'account/register.html', {
        'form': form,
        'roles': Role.objects.all()  # Ajouter les rôles disponibles
    })


@login_required
def profile_view(request):
    """Vue de profil utilisateur"""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)
        user.address = request.POST.get('address', user.address)
        user.save()
        messages.success(request, 'Profil mis à jour avec succès')
        return redirect('profile')
    
    return render(request, 'account/profile.html')
