from fastapi import HTTPException, status


class CertificateFormatException(HTTPException):
    def __init__(self, message="Only .pdf extensions are allowed"):
        super(CertificateFormatException, self).__init__(detail=message, status_code=status.HTTP_400_BAD_REQUEST)
