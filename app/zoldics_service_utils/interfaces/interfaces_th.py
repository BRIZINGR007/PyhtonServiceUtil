from typing import TypedDict, Required, Dict

from typing import TypedDict, List, Dict, Required


class Jwk_TH(TypedDict, total=False):
    alg: Required[str]
    e: str
    kid: Required[str]
    kty: str
    n: str
    use: str


class Headers_TH(TypedDict):
    correlationid: str
    username: str
    authorization: str


class SQSClientCallBackResponse_TH(TypedDict):
    allSuccess: bool
    correlationid: str


class LLM_HyperParameters_TH(TypedDict, total=False):
    max_gen_len: int
    temperature: Required[float]
    top_p: Required[float]
    top_k: int
    max_tokens: int
    stop: List[str]


class BedrockPayload_TH(TypedDict, total=False):
    prompt: str
    max_gen_len: int
    temperature: Required[float]
    top_p: Required[float]
    top_k: int
    max_tokens: int
    stop: List[str]


class LLM_SpecialTokens_TH(TypedDict):
    bos_token: str
    content_start_token: str
    content_end_token: str
    eos_token: str


class LLM_ModelConfig_TH(TypedDict):
    modelName: str
    providerName: str
    responseStreamingSupported: bool
    payload_format: BedrockPayload_TH
    special_tokens: LLM_SpecialTokens_TH


class LLM_PromptTemplates_TH(TypedDict, total=False):
    system_prompt: str
    user_prompt: Required[str]
    user_prompt_1: str
    base_token_count: int
