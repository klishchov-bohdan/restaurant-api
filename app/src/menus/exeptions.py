from fastapi import HTTPException, status


class MenuNotFoundError(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = 'menu not found'
