from fastapi import HTTPException

class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Taki użytkownik nie istnieje")

class UserAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Użytkownik o podanej nazwie już istnieje")

class EmailAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Podany email już istnieje")

class UserNotAuthorizedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Użytkownik nie jest zalogowany")

class UserNotAdminException(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail="Użytkownik nie jest administratorem")
