try:
    from .local import ApplicationSettings
except ImportError:
    from .base import ApplicationSettings

application = ApplicationSettings()
