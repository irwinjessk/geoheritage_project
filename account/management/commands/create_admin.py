from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Crée un superutilisateur par défaut'

    def handle(self, *args, **options):
        User = get_user_model()
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@gmail.com',
                password='admin'
            )
            self.stdout.write(
                self.style.SUCCESS('✅ Superutilisateur admin créé avec succès')
            )
        else:
            self.stdout.write(
                self.style.WARNING('ℹ️ L\'utilisateur admin existe déjà')
            )
