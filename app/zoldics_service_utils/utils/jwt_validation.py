from ast import List
from functools import lru_cache
import json
from jwcrypto import jwk
import jwt
from typing import Dict, List, Optional

from ..constants.errors import ErrorEnums

from ..utils.env_initlializer import EnvStore
from ..utils.exceptions import JwtValidationError
from ..interfaces.interfaces_th import Jwk_TH


class JwtValdationUtils:
    JWT_ALGORITHM = "RS256" if EnvStore().auth_token_algorithm == "RS256" else "HS256"

    @staticmethod
    def is_token_expired(token: str) -> bool:
        try:
            JwtValdationUtils.validate_token(token, verify_exp=True)
            return False
        except JwtValidationError as e:
            if e == ErrorEnums.TOKEN_EXPIRED:
                return True
            raise e

    @lru_cache(maxsize=1)
    @staticmethod
    def __load_jwks() -> List[Jwk_TH]:
        return json.loads(EnvStore().jwks)

    @classmethod
    def _get_public_key(cls, kid: str) -> Optional[str]:
        public_key = next((key for key in cls.__load_jwks() if key["kid"] == kid), None)
        if public_key:
            return jwk.JWK(**public_key).export_to_pem().decode("utf-8")
        return None

    @classmethod
    def validate_token(
        cls,
        token: str,
        verify_exp: bool = False,
        verify_aud: bool = False,
    ) -> Dict:
        try:
            JWT_ALGORITHM = (
                "RS256" if EnvStore().auth_token_algorithm == "RS256" else "HS256"
            )
            default_options = dict()
            if not verify_exp:
                default_options.update(verify_exp=False)
            if not verify_aud:
                default_options.update(verify_aud=False)

            unverified_header = jwt.get_unverified_header(token)
            public_key = cls._get_public_key(unverified_header["kid"])

            if not public_key:
                raise ValueError("No matching public key found")

            return jwt.decode(
                token,
                public_key,
                algorithms=[JWT_ALGORITHM],
                options=default_options,
            )
        except jwt.ExpiredSignatureError:
            raise JwtValidationError(ErrorEnums.TOKEN_EXPIRED)
        except jwt.InvalidSignatureError:
            raise JwtValidationError(ErrorEnums.INVALID_SIGNATURE)
        except jwt.InvalidAudienceError:
            raise JwtValidationError(ErrorEnums.INVALID_AUDIENCE)
        except jwt.InvalidIssuerError:
            raise JwtValidationError(ErrorEnums.INVALID_ISSUER)
        except jwt.DecodeError:
            raise JwtValidationError(ErrorEnums.MALFORMED_TOKEN)
        except jwt.PyJWTError as e:
            raise JwtValidationError(f"Invalid token: {str(e)}")
        except Exception:
            raise Exception(ErrorEnums.JWT_GENERAL_ERROR)
