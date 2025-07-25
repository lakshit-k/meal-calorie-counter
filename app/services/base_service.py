import requests
from urllib.parse import urljoin
import httpx

class BaseService:
    def __init__(self, base_url: str = ""):
        self.base_url = base_url
        self.endpoint = ""
        self.params = {}
        self.data = {}
        self.headers = {}
        self.method = "GET"

    def set_endpoint(self, endpoint: str):
        self.endpoint = endpoint
        return self

    def set_params(self, params: dict):
        self.params = params
        return self

    def set_data(self, data: dict):
        self.data = data
        return self

    def set_headers(self, headers: dict):
        self.headers = headers
        return self

    def set_method(self, method: str):
        self.method = method.upper()
        return self

    def generate_url(self):
        return urljoin(self.base_url, self.endpoint)

    def make_request(self):
        url = self.generate_url()
        response = requests.request(
            method=self.method,
            url=url,
            params=self.params if self.method == "GET" else None,
            data=self.data if self.method in ["POST", "PUT", "PATCH"] else None,
            headers=self.headers
        )
        return response

    async def async_make_request(self):
        url = self.generate_url()
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=self.method,
                url=url,
                params=self.params if self.method == "GET" else None,
                data=self.data if self.method in ["POST", "PUT", "PATCH"] else None,
                headers=self.headers
            )
            return response

    def invoke(self):
        """
        Main method to be called for making the request synchronously.
        """
        return self.make_request()

    async def async_invoke(self):
        """
        Main method to be called for making the request asynchronously.
        """
        return await self.async_make_request()
