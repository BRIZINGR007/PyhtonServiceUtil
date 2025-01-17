from typing import TypedDict, Required, Dict


class Jwk_TH(TypedDict, total=False):
    alg: Required[str]
    e: str
    kid: Required[str]
    kty: str
    n: str
    use: str


class Headers_TH(TypedDict, total=False):
    correlationid: str
    username: str
    authorization: str


class SSEMessage_TH(TypedDict):
    event: str
    data: Dict[str, str]


class SQSClientCallBackResponse_TH(TypedDict):
    allSuccess: bool
    correlationid: str
