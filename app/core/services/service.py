class Service:
    _instance = None

    def __str__(self):
        return "Service class (core): " + self.__class__.__name__

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance
