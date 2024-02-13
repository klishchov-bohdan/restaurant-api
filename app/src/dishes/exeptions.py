from fastapi import HTTPException, status


class DishNotFoundError(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = 'dish not found'
