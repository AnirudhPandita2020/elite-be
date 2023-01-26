from fastapi import HTTPException, status


class CertificateFormatException(HTTPException):
    def __init__(self, message="Only .pdf extensions are allowed"):
        super(CertificateFormatException, self).__init__(detail=message, status_code=status.HTTP_400_BAD_REQUEST)


class CertificateNotPresentException(HTTPException):
    def __init__(self, message="Certificate of the current type is not present. Consider adding one"):
        super().__init__(detail=message, status_code=status.HTTP_404_NOT_FOUND)


class CertificateValidityException(HTTPException):
    def __init__(self, message="Certificate Validity should not be less than the current validity date"):
        super().__init__(detail=message, status_code=status.HTTP_406_NOT_ACCEPTABLE)
