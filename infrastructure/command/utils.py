def get_inject_dependency():
    from infrastructure.dependencies.application_container import ApplicationDependenciesContainer

    di = ApplicationDependenciesContainer()
    di.configs.from_dict(
        {"api_multi_url": "https://multi-univ.russu.xyz/", "api_single_url": "https://single-univ.russu.xyz/"}
    )
    from infrastructure.command import tasks

    di.wire(modules=[tasks])
    return di
