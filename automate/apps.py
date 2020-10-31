from django.apps import AppConfig


class AutomateConfig(AppConfig):
    name = 'automate'

    #for registring signals
    def ready(self):
        import automate.signals