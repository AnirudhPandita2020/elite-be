from fastapi import HTTPException, status


class UserAlreadyPresentException(HTTPException):
    def __init__(self, message="User already present"):
        super().__init__(detail=message, status_code=status.HTTP_409_CONFLICT)


class UserNotActiveException(HTTPException):
    def __init__(self, message="The user is not active.Contact the administrator"):
        super().__init__(detail=message, status_code=status.HTTP_406_NOT_ACCEPTABLE)


class UserCredentialException(HTTPException):
    def __init__(self, message="Credential Validation Failed"):
        super(UserCredentialException, self).__init__(detail=message, status_code=status.HTTP_403_FORBIDDEN,
                                                      headers={"WWW-Authenticate": "Bearer"})


class NotValidEmailException(HTTPException):
    def __init__(self, message="User creation failed"):
        super().__init__(detail=message, status_code=status.HTTP_403_FORBIDDEN)


class UserAccessDeniedException(HTTPException):
    def __init__(self, message="Access Denied"):
        super().__init__(detail=message, status_code=status.HTTP_403_FORBIDDEN)
