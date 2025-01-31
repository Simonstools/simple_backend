import httpx
from config import settings
from fastapi import HTTPException

class WrongMethod(Exception):
    def __init__(self, method_name):
        self.method_name = method_name
        self.message = f"Wrong method {method_name=} passed"
        super().__init__(self.message)

class JsonBin:
    ROOT_URL = settings.JSONBIN_ROOT_URL
    HEADERS = {
        "X-Master-Key": settings.JSONBIN_API_KEY,
        "Content-Type": "application/json"
    }

    def __init__(self):
        pass

    @classmethod
    def __make_request(
            cls,
            method: str,
            route: str,
            data=None
    ) -> dict:
        if method not in ['GET', 'POST', 'PUT', 'DELETE']:
            raise WrongMethod(method)
        with httpx.Client() as client:
            resp = client.request(
                method=method,
                url=f"{cls.ROOT_URL}{route}",
                headers=cls.HEADERS,
                json=data
            )
            if resp.status_code != 200:
                raise HTTPException(
                    status_code=resp.status_code,
                    detail=resp.text
                )
        return resp.json()

    @classmethod
    def create_bin(cls, data: dict):
        method = 'POST'
        route = '/b'
        return cls.__make_request(method, route, data)

    @classmethod
    def read_bin(cls, bin_id: str):
        method = 'GET'
        route = f"/b/{bin_id}"
        return cls.__make_request(method, route)

    @classmethod
    def update_bin(cls, bin_id: str, data: dict):
        method = 'PUT'
        route = f"/b/{bin_id}"
        return cls.__make_request(method, route, data)

    @classmethod
    def delete_bin(cls, bin_id: str):
        method = 'DELETE'
        route = f"/b/{bin_id}"
        return cls.__make_request(method, route)
