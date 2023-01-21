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
    def __init__(self, message="Please provide the company email"):
        super().__init__(detail=message, status_code=status.HTTP_403_FORBIDDEN)


class UserAccessDeniedException(HTTPException):
    def __init__(self, message="Access Denied"):
        super().__init__(detail=message, status_code=status.HTTP_403_FORBIDDEN)


class UserPasswordWeakException(HTTPException):
    def __init__(self, message="The given password is weak.Consider adding a strong one"):
        super().__init__(detail=message, status_code=status.HTTP_400_BAD_REQUEST)
