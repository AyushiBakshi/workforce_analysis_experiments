from django.apps import AppConfig
from .lookup import SplitAndContains, SplitAndLT, SplitAndGT

class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        import api.signals  
        from django.db.models.fields import Field
        Field.register_lookup(SplitAndContains)
        Field.register_lookup(SplitAndLT)
        Field.register_lookup(SplitAndGT)


