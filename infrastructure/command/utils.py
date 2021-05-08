from infrastructure.settings import application as conf

SETTINGS_LOGGER = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"default": {"()": "infrastructure.logs.JsonFormatter"}},
    "handlers": {"default": {"class": "logging.StreamHandler", "formatter": "default"}},
    "loggers": {
        "": {"level": "DEBUG", "handlers": ["default"]},
        "databases": {"level": "INFO", "handlers": ["default"]},
    },
}


def get_inject_dependency():
    from infrastructure.dependencies.application_container import ApplicationDependenciesContainer

    di = ApplicationDependenciesContainer()
    di.configs.from_dict({"api_multi_url": conf.API_MULTI_URL, "api_single_url": conf.API_SINGLE_URL})
    from infrastructure.command import tasks
    from infrastructure.dependencies import dependencies_function
    from infrastructure.web import views

    di.wire(modules=[tasks, dependencies_function, views])
    return di
