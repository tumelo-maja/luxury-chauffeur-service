from django.apps import AppConfig


class TripsConfig(AppConfig):
    """
    Configuration for the `trips` application.

    Attributes
    ----------
    default_auto_field : str
        The type of primary key field to use for models by default.
    name : str
        name of the application.
    """        
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trips'

