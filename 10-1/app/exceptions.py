class CustomExceptionA(Exception):
    def __init__(self, message: str = "Ошибка валидации данных"):
        self.message = message
        self.status_code = 400
        super().__init__(self.message)


class CustomExceptionB(Exception):
    def __init__(self, message: str = "Ресурс не найден"):
        self.message = message
        self.status_code = 404
        super().__init__(self.message)