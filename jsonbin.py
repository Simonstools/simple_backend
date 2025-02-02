import logging

import httpx

from config import settings

from fastapi import HTTPException

from utils import check_route


class JsonBin:
    ROOT_URL = settings.JSONBIN_ROOT_URL
    HEADERS = {
        "X-Master-Key": settings.JSONBIN_API_KEY,
        "Content-Type": "application/json"
    }

    @classmethod
    def __make_request(
            cls,
            method: str,
            route: str,
            data=None
    ) -> dict:
        with httpx.Client() as client:
            route = check_route(route)
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
