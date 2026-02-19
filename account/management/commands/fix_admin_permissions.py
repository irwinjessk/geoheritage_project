from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from account.models import Role
from django.db.models import Min


class Command(BaseCommand):
    help = 'Fix admin permissions in production'

    def handle(self, *args, **options):
        User = get_user_model()
        
        try:
            admin = User.objects.get(username='admin')
            
            # Créer le rôle admin s'il n'existe pas
            admin_role, created = Role.objects.get_or_create(
                name='admin',
                defaults={
                    'description': 'Administrateur système',
                    'level': 1
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS('✅ Rôle admin créé'))
            
            # Assigner le rôle admin
            if not admin.roles.filter(name='admin').exists():
                admin.roles.add(admin_role)
                self.stdout.write(self.style.SUCCESS('✅ Rôle admin assigné'))
            else:
                self.stdout.write(self.style.WARNING('ℹ️ Rôle admin déjà assigné'))
            
            # Vérifier le niveau final
            level = admin.roles.aggregate(min_level=Min('level'))['min_level'] or 999
            self.stdout.write(
                self.style.SUCCESS(f'✅ Niveau final de l\'admin: {level}')
            )
            
            # Vérifier les permissions
            can_create = level <= 3
            can_edit_all = level <= 2
            can_delete_all = level <= 2
            
            self.stdout.write(f'Peut créer patrimoine: {can_create}')
            self.stdout.write(f'Peut modifier tous: {can_edit_all}')
            self.stdout.write(f'Peut supprimer tous: {can_delete_all}')
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ Utilisateur admin non trouvé'))
