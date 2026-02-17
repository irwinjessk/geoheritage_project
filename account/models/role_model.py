from django.db import models

class Role(models.Model):
    ADMIN = 'admin'
    MODERATEUR = 'moderateur'
    CONTRIBUTEUR = 'contributeur'
    UTILISATEUR = 'utilisateur'
    
    ROLE_CHOICES = [
        (ADMIN, 'Administrateur'),
        (MODERATEUR, 'Modérateur'),
        (CONTRIBUTEUR, 'Contributeur'),
        (UTILISATEUR, 'Utilisateur'),
    ]
    
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)
    level = models.IntegerField(default=4)  # 1=admin, 2=modo, 3=contrib, 4=user
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.get_name_display()
    
    class Meta:
        ordering = ['level']  # Ordre hiérarchique
