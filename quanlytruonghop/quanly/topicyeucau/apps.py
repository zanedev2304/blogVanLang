from django.apps import AppConfig


class TopicyeucauConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'topicyeucau'

    def ready(self):
        import topicyeucau.signals



