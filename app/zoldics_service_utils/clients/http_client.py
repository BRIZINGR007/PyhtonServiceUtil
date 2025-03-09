import requests
from typing import Optional, Dict
from ..utils.env_initlializer import EnvStore

"""
    A versatile HTTP client for making inter-service calls or external API requests.

    Attributes:
        headers (Dict[str, str]): Headers to be included in the HTTP request.
        path (str): The endpoint path for the request.
        body (Optional[Dict]): The request body for methods like POST, PATCH, PUT.
        path_params (Optional[Dict[str, str]]): Path parameters to be substituted in the URL.
        query_params (Optional[Dict[str, str]]): Query parameters to be appended to the URL.
        localhost_interservice_call (bool): If True, the request is made to localhost for development purposes.
        portNumber (Optional[str]): The port number to use when making localhost requests.
"""


class HttpClient:
    def __init__(
        self,
        headers: Dict[str, str],
        path: str,
        body=None,
        path_params: Optional[Dict[str, str]] = None,
        query_params: Optional[Dict[str, str]] = None,
        localhost_interservice_call: bool = False,
        portNumber: Optional[str] = None,
    ) -> None:
        self.__localhost_interservice_call = localhost_interservice_call
        self.__domain: str = EnvStore().domain
        self.__portnumber: Optional[str] = portNumber
        self.__headers = headers
        self.__path = path
        self.__body = body
        self.__path_params = path_params
        self.__query_params = query_params

    def __construct_url(self) -> str:
        base_url = (
            f"https://{self.__domain}/"
            if not self.__localhost_interservice_call
            else f"http://localhost:{self.__portnumber}/"
        )
        url = base_url + self.__path
        if self.__path_params:
            url = url.format(**self.__path_params)
        return url

    def __send_request(self, method: str) -> requests.Response:
        url: str = self.__construct_url()
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.__headers,
                params=self.__query_params,
                json=self.__body,
            )
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            return response
        except requests.exceptions.RequestException as e:
            raise

    def get(self) -> requests.Response:
        return self.__send_request("GET")

    def post(self) -> requests.Response:
        return self.__send_request("POST")

    def patch(self) -> requests.Response:
        return self.__send_request("PATCH")

    def put(self) -> requests.Response:
        return self.__send_request("PUT")

    def delete(self) -> requests.Response:
        return self.__send_request("DELETE")
