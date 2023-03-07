from django.apps import AppConfig


class ManageuserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'manageUser'



    def ready(self):
        import manageUser.signals