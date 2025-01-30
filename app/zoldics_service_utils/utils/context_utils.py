from typing import cast

from ..interfaces.interfaces_pd import Headers_PM
from ..interfaces.interfaces_th import Headers_TH
from ..context.vars import headers_context


class ContextUtils:
    @staticmethod
    def get_header_details() -> Headers_PM:
        return cast(Headers_PM, headers_context.get())
