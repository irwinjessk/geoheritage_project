from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    def ready(self):
        import account.signals
        # Créer l'admin par défaut au démarrage de l'application
        self.create_default_user()

    def create_default_user(self):
        """
        Crée un superutilisateur par défaut au démarrage de l'application.
        Cette méthode est appelée chaque fois que l'application démarre.
        """
        from django.contrib.auth import get_user_model
        from django.db.utils import OperationalError
        
        User = get_user_model()
        
        try:
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@gmail.com',
                    password='admin'
                )
                print("✅ Superutilisateur par défaut créé (admin / admin)")
            else:
                print("ℹ️ L'utilisateur admin existe déjà")
        except OperationalError:
            # La base de données n'est pas encore prête (pendant les migrations)
            pass
