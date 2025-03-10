from typing import Optional, cast
from ..ioc.singleton import SingletonMeta


class EnvStore(metaclass=SingletonMeta):
    def __init__(self) -> None:
        # Service  Utils  required envs
        self._aws_region_name: Optional[str] = None
        self._aws_access_key_id: Optional[str] = None
        self._aws_secret_access_key: Optional[str] = None
        self._domain: Optional[str] = None
        self._servicename: Optional[str] = None
        self._environment: Optional[str] = None
        self._dbname: Optional[str] = None
        self._jwks: Optional[str] = None
        self._auth_token_algorithm: Optional[str] = None
        # Service  Utils  required envs
        self._redis_uri: Optional[str] = None
        self._mongo_uri: Optional[str] = None
        self._service_port: Optional[str] = None
        self._uvicorn_workers: Optional[str] = None
        self._cognito_user_poolid: Optional[str] = None
        self._cognito_clientid: Optional[str] = None
        self._cognito_client_secret: Optional[str] = None
        self._google_config: Optional[str] = None
        self._xapi_key_1: Optional[str] = None
        self._xapi_key_2: Optional[str] = None

    @property
    def xapi_key_1(self) -> str:
        return cast(str, self._xapi_key_1)

    @xapi_key_1.setter
    def xapi_key_1(self, value: Optional[str]) -> None:
        self._xapi_key_1 = value

    @property
    def xapi_key_2(self) -> str:
        return cast(str, self._xapi_key_2)

    @xapi_key_2.setter
    def xapi_key_2(self, value: Optional[str]) -> None:
        self._xapi_key_2 = value

    def validate_env_variables(self) -> None:
        missing_vars = []

        required_vars = {
            "AWS_REGION_NAME": self._aws_region_name,
            "AWS_ACCESS_KEY_ID": self._aws_access_key_id,
            "AWS_SECRET_ACCESS_KEY": self._aws_secret_access_key,
            "DOMAIN": self._domain,
            "SERVICE_NAME": self._servicename,
            "ENVIRONMENT": self._environment,
            "DB_NAME": self._dbname,
            "JWKS": self._jwks,
            "AUTH_TOKEN_ALGORITHM": self._auth_token_algorithm,
        }

        for var_name, value in required_vars.items():
            if not value:
                missing_vars.append(var_name)

        if missing_vars:
            raise ValueError(
                f"Missing environment variables: {', '.join(missing_vars)}"
            )

    @property
    def google_config(self) -> str:
        return cast(str, self._google_config)

    @google_config.setter
    def google_config(self, value: Optional[str]) -> None:
        self._google_config = value

    @property
    def cognito_user_poolid(self) -> str:
        return cast(str, self._cognito_user_poolid)

    @cognito_user_poolid.setter
    def cognito_user_poolid(self, value: Optional[str]) -> None:
        self._cognito_user_poolid = value

    @property
    def cognito_clientid(self) -> str:
        return cast(str, self._cognito_clientid)

    @cognito_clientid.setter
    def cognito_clientid(self, value: Optional[str]) -> None:
        self._cognito_clientid = value

    @property
    def cognito_client_secret(self) -> str:
        return cast(str, self._cognito_client_secret)

    @cognito_client_secret.setter
    def cognito_client_secret(self, value: Optional[str]) -> None:
        self._cognito_client_secret = value

    @property
    def uvicorn_workers(self) -> str:
        return cast(str, self._uvicorn_workers)

    @uvicorn_workers.setter
    def uvicorn_workers(self, value: str) -> None:
        self._uvicorn_workers = value

    @property
    def service_port(self) -> str:
        return cast(str, self._service_port)

    @service_port.setter
    def service_port(self, value: str) -> None:
        self._service_port = value

    @property
    def mongo_uri(self) -> str:
        return cast(str, self._mongo_uri)

    @mongo_uri.setter
    def mongo_uri(self, value: str) -> None:
        self._mongo_uri = value

    @property
    def redis_uri(self) -> str:
        return cast(str, self._redis_uri)

    @redis_uri.setter
    def redis_uri(self, value: str) -> None:
        self._redis_uri = value

    @property
    def jwks(self) -> str:
        return cast(str, self._jwks)

    @jwks.setter
    def jwks(self, value: str) -> None:
        self._jwks = value

    @property
    def dbname(self) -> str:
        return cast(str, self._dbname)

    @dbname.setter
    def dbname(self, value: str) -> None:
        self._dbname = value

    @property
    def environment(self) -> str:
        return cast(str, self._environment)

    @environment.setter
    def environment(self, value: str) -> None:
        self._environment = value

    @property
    def servicename(self) -> str:
        return cast(str, self._servicename)

    @servicename.setter
    def servicename(self, value: str) -> None:
        self._servicename = value

    @property
    def domain(self) -> str:
        return cast(str, self._domain)

    @domain.setter
    def domain(self, value: str) -> None:
        self._domain = value

    @property
    def aws_region_name(self) -> str:
        return cast(str, self._aws_region_name)

    @aws_region_name.setter
    def aws_region_name(self, value: str) -> None:
        self._aws_region_name = value

    @property
    def aws_access_key_id(self) -> str:
        return cast(str, self._aws_access_key_id)

    @aws_access_key_id.setter
    def aws_access_key_id(self, value: str) -> None:
        self._aws_access_key_id = value

    @property
    def aws_secret_access_key(self) -> str:
        return cast(str, self._aws_secret_access_key)

    @aws_secret_access_key.setter
    def aws_secret_access_key(self, value: str) -> None:
        self._aws_secret_access_key = value

    @property
    def auth_token_algorithm(self) -> str:
        return cast(str, self._auth_token_algorithm)

    @auth_token_algorithm.setter
    def auth_token_algorithm(self, value: str) -> None:
        self._auth_token_algorithm = value
