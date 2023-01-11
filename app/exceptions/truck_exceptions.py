from fastapi import HTTPException, status


class TruckAlreadyPresentException(HTTPException):
    def __init__(self, message="Truck is already present"):
        super(TruckAlreadyPresentException, self).__init__(detail=message, status_code=status.HTTP_409_CONFLICT)


class TruckNotPresentException(HTTPException):
    def __init__(self, message="Truck is not available"):
        super(TruckNotPresentException, self).__init__(detail=message, status_code=status.HTTP_404_NOT_FOUND)


class InvalidSiteException(HTTPException):
    def __init__(self, site: str):
        super().__init__(detail=f'Invalid site {site}.Contact the administrator if you think this is a mistake',
                         status_code=status.HTTP_400_BAD_REQUEST)
