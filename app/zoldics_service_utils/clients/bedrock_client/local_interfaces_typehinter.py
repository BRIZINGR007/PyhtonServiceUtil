from typing import TypedDict, List, Dict

from ...clients.bedrock_client.foundation_models import (
    FoundationModels,
)

from ...interfaces.interfaces_th import LLM_HyperParameters_TH


class LLM_ClientPayload_TH(TypedDict):
    messages: List[Dict[str, str]]
    model_hyperparameters: LLM_HyperParameters_TH
    modelId: FoundationModels
