from django.db import models
from account.models import User


class Patrimoine(models.Model):
    TYPE_CHOICES = [
        ('monument', 'Monument'),
        ('musee', 'Musée'),
        ('site_naturel', 'Site naturel'),
        ('batiment', 'Bâtiment historique'),
    ]

    nom = models.CharField(max_length=200)
    description = models.TextField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    ville = models.CharField(max_length=100)
    date_creation = models.DateField()
    photo_url = models.URLField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patrimoines')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom
