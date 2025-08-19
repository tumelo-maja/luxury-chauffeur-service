from django.apps import AppConfig


class HomeConfig(AppConfig):
    """
    Configuration for the `home` application.

    Attributes
    ----------
    default_auto_field : str
        The type of primary key field to use for models by default.
    name : str
        name of the application.
    """       
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
