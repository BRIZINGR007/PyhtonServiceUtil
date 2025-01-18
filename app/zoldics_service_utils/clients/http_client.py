import requests
from decouple import config
import uuid
from typing import Optional, Dict
from logging.base_logger import APP_LOGGER


class HttpClient:
    def __init__(
        self,
        headers: Dict[str, str],
        path: str,
        body=None,
        correlationid: Optional[str] = None,
        path_params: Optional[Dict[str, str]] = None,
        query_params: Optional[Dict[str, str]] = None,
        interServiceCall: bool = False,
        localhostCall: bool = False,
        portNumber: str = str(config("PORT")),
    ) -> None:
        self.interServiceCall = interServiceCall
        self.localhostCall = localhostCall
        self.__request_id = str(uuid.uuid4())
        self.__environment: str = str(config("ENVIRONMENT"))
        self.__domain: str = str(config("DOMAIN"))
        self.__portnumber: str = portNumber
        self.__headers = headers
        self.__path = path
        self.__body = body
        self.__path_params = path_params
        self.__query_params = query_params
        if correlationid is None:
            self.__correlationid = str(uuid.uuid4())
        else:
            self.__correlationid = correlationid
        self.__headers["correlationid"] = self.__correlationid

    def __construct_url(self) -> str:
        base_url = (
            f"https://{self.__environment}{self.__domain}/"
            if self.interServiceCall
            else f"http://localhost:{self.__portnumber}/"
        )
        url = base_url + self.__path
        if self.__path_params:
            url = url.format(**self.__path_params)
        return url

    def __send_request(self, method: str) -> requests.Response:
        url: str = self.__construct_url()
        APP_LOGGER.info(
            f"Sending {method} request to {url} with correlationId = {self.__correlationid} and requestid = {self.__request_id}"
        )
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.__headers,
                params=self.__query_params,
                json=self.__body,
            )
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            APP_LOGGER.info(
                f"Received response with status code {response.status_code} with correlationid = {self.__correlationid} and requestid  = {self.__request_id}"
            )
            return response
        except requests.exceptions.RequestException as e:
            APP_LOGGER.error(
                f"Request failed with correlationid = {self.__correlationid} and requestid = {self.__request_id}. Error: {str(e)}"
            )
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
