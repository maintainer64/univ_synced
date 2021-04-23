class ApiErrorBase(Exception):
    code = None
    message = None

    def __init__(self, code: int, message: str, meta: dict = None):
        self.code = code or self.__class__.code
        self.message = message or self.__class__.message
        self.meta = meta
