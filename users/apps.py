from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Configuration for the `users` application.

    Attributes
    ----------
    default_auto_field : str
        The type of primary key field to use for models by default.
    name : str
        name of the application.
    """    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        """
        Triggered when Django starts to defined and register the signal handlers in `users.signals`.
        """        
        import users.signals
