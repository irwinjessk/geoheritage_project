from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages
from django.db import models

def get_user_level(user):
    """Récupérer le niveau le plus bas (plus élevé) de l'utilisateur"""
    if not user.is_authenticated:
        return 999
    return user.roles.aggregate(models.Min('level'))['level__min'] or 999

def role_required(*allowed_roles):
    """
    Décorateur pour vérifier si l'utilisateur a le rôle requis
    Usage: @role_required('admin', 'moderateur')
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('account:login')
            
            # Vérifier les rôles de l'utilisateur
            user_roles = request.user.roles.values_list('name', flat=True)
            
            # Vérifier si l'utilisateur a au moins un des rôles autorisés
            if not any(role in user_roles for role in allowed_roles):
                messages.error(request, f"Accès refusé. Rôles requis: {', '.join(allowed_roles)}")
                return redirect('heritage:list')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def level_required(max_level):
    """
    Décorateur pour vérifier le niveau de permission
    Usage: @level_required(3)  # Niveau 3 ou supérieur (contributeur+)
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('account:login')
            
            user_level = get_user_level(request.user)
            if user_level > max_level:
                messages.error(request, f"Permissions insuffisantes. Niveau requis: {max_level} ou supérieur")
                return redirect('heritage:list')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def admin_required(view_func):
    """Décorateur pour les administrateurs uniquement (level 1)"""
    return level_required(1)(view_func)

def moderateur_required(view_func):
    """Décorateur pour les modérateurs et administrateurs (level 2+)"""
    return level_required(2)(view_func)

def contributeur_required(view_func):
    """Décorateur pour les contributeurs, modérateurs et administrateurs (level 3+)"""
    return level_required(3)(view_func)

def utilisateur_required(view_func):
    """Décorateur pour tous les utilisateurs authentifiés (level 4+)"""
    return level_required(4)(view_func)

def can_edit_patrimoine(view_func):
    """
    Décorateur pour vérifier si l'utilisateur peut modifier un patrimoine
    - Admin (level 1) : peut modifier tous les patrimoines
    - Modérateur (level 2) : peut modifier tous les patrimoines
    - Contributeur (level 3) : peut modifier uniquement ses patrimoines
    - Utilisateur (level 4) : ne peut rien modifier
    """
    @wraps(view_func)
    def _wrapped_view(request, pk=None, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account:login')
        
        from heritage.models import Patrimoine
        
        # Récupérer le patrimoine si l'ID est fourni
        patrimoine = None
        if pk:
            try:
                patrimoine = Patrimoine.objects.get(pk=pk)
            except Patrimoine.DoesNotExist:
                messages.error(request, "Patrimoine introuvable")
                return redirect('heritage:list')
        
        user_level = get_user_level(request.user)
        
        # Admin et modérateur peuvent tout modifier (level 1 et 2)
        if user_level <= 2:
            return view_func(request, patrimoine, *args, **kwargs)
        
        # Contributeur peut modifier uniquement ses patrimoines (level 3)
        if user_level == 3 and patrimoine and patrimoine.created_by == request.user:
            return view_func(request, patrimoine, *args, **kwargs)
        
        # Utilisateur ne peut rien modifier (level 4)
        if patrimoine:
            messages.error(request, "Vous n'avez pas les permissions pour modifier ce patrimoine")
        return redirect('heritage:detail', pk=patrimoine.pk) if patrimoine else redirect('heritage:list')
    
    return _wrapped_view
