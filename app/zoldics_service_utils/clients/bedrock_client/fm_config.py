from typing import Dict
from ...interfaces.interfaces_th import (
    LLM_ModelConfig_TH,
    BedrockPayload_TH,
    LLM_SpecialTokens_TH,
)

FMS_BEDROCK: Dict[str, LLM_ModelConfig_TH] = {
    "meta.llama3-8b-instruct-v1:0": LLM_ModelConfig_TH(
        modelName="Llama 3 8B Instruct",
        providerName="Meta",
        responseStreamingSupported=True,
        payload_format=BedrockPayload_TH(
            prompt="", max_gen_len=64, temperature=0.6, top_p=0.6
        ),
        special_tokens=LLM_SpecialTokens_TH(
            bos_token="<|begin_of_text|>",
            content_start_token="<|start_header_id|>{role}<|end_header_id|>",
            content_end_token="<|eot_id|>",
            eos_token="<|end_of_text|>",
        ),
    ),
    "meta.llama3-70b-instruct-v1:0": LLM_ModelConfig_TH(
        modelName="Llama 3 70B Instruct",
        providerName="Meta",
        responseStreamingSupported=False,
        payload_format=BedrockPayload_TH(
            prompt="", max_gen_len=64, temperature=0.6, top_p=0.6
        ),
        special_tokens=LLM_SpecialTokens_TH(
            bos_token="<|begin_of_text|>",
            content_start_token="<|start_header_id|>{role}<|end_header_id|>",
            content_end_token="<|eot_id|>",
            eos_token="<|end_of_text|>",
        ),
    ),
    "meta.llama3-1-8b-instruct-v1:0": LLM_ModelConfig_TH(
        modelName="Llama 3 8B Instruct",
        providerName="Meta",
        responseStreamingSupported=True,
        payload_format=BedrockPayload_TH(
            prompt="", max_gen_len=64, temperature=0.6, top_p=0.6
        ),
        special_tokens=LLM_SpecialTokens_TH(
            bos_token="<|begin_of_text|>",
            content_start_token="<|start_header_id|>{role}<|end_header_id|>",
            content_end_token="<|eot_id|>",
            eos_token="<|end_of_text|>",
        ),
    ),
    "meta.llama3-1-70b-instruct-v1:0": LLM_ModelConfig_TH(
        modelName="Llama 3 70B Instruct",
        providerName="Meta",
        responseStreamingSupported=False,
        payload_format=BedrockPayload_TH(
            prompt="", max_gen_len=64, temperature=0.6, top_p=0.6
        ),
        special_tokens=LLM_SpecialTokens_TH(
            bos_token="<|begin_of_text|>",
            content_start_token="<|start_header_id|>{role}<|end_header_id|>",
            content_end_token="<|eot_id|>",
            eos_token="<|end_of_text|>",
        ),
    ),
    "mistral.mistral-7b-instruct-v0:2": LLM_ModelConfig_TH(
        modelName="Mistral 7B Instruct",
        providerName="Mistral AI",
        responseStreamingSupported=True,
        payload_format=BedrockPayload_TH(
            prompt="",
            max_tokens=64,
            temperature=0.6,
            top_p=0.6,
            top_k=6,
            # stop=["."],
        ),
        special_tokens=LLM_SpecialTokens_TH(
            bos_token="<s>",
            content_start_token="[INST]",
            content_end_token="[/INST]",
            eos_token="</s>",
        ),
    ),
    "mistral.mixtral-8x7b-instruct-v0:1": LLM_ModelConfig_TH(
        modelName="Mixtral 8x7B Instruct",
        providerName="Mistral AI",
        responseStreamingSupported=False,
        payload_format=BedrockPayload_TH(
            prompt="",
            max_tokens=64,
            temperature=0.6,
            top_p=0.6,
            top_k=6,
            # stop=["."],
        ),
        special_tokens=LLM_SpecialTokens_TH(
            bos_token="<s>",
            content_start_token="[INST]",
            content_end_token="[/INST]",
            eos_token="</s>",
        ),
    ),
}
