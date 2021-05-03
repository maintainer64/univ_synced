class DepartmentException(ValueError):
    ...


class DepartmentNotFound(DepartmentException):
    ...


class DepartmentNotCreated(DepartmentException):
    ...
