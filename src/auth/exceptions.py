from fastapi import HTTPException

class WrongPasswordException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Nieprawidłowe hasło")

class InvalidTokenException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Nieprawidłowy token")