from fastapi import HTTPException, status


class TruckAlreadyPresentException(HTTPException):
    def __init__(self, message="Truck is already present"):
        super(TruckAlreadyPresentException, self).__init__(detail=message, status_code=status.HTTP_409_CONFLICT)


class TruckNotPresentException(HTTPException):
    def __init__(self, message="Truck is not available"):
        super(TruckNotPresentException, self).__init__(detail=message, status_code=status.HTTP_404_NOT_FOUND)
