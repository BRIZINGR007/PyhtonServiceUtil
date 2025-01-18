from typing import cast
from ..interfaces.interfaces_th import Headers_TH
from ..context.vars import headers_context


class ContextUtils:
    @staticmethod
    def get_user_details_from_headers() -> Headers_TH:
        return cast(Headers_TH, headers_context.get())
