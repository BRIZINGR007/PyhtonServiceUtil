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

    def validate_env_variables(self) -> None:
        missing_vars = []

        for attr in self.__dict__:
            if getattr(self, attr) is None:
                missing_vars.append(attr.upper())

        if missing_vars:
            raise ValueError(
                f"Missing environment variables: {', '.join(missing_vars)}"
            )

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
