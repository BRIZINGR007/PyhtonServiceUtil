# PythonServiceUtil

PythonServiceUtil is a utility library designed to streamline Python-based microservice development. It offers robust support for REST inter-service calls, AWS SQS, Redis, and MongoDB, enabling faster, more efficient development workflows.

## Features

- **REST Inter-service Calls**: Simplifies HTTP communication between services.
- **AWS SQS Integration**: Enhances message queue operations.
- **Redis Support**: Provides efficient caching and data storage.
- **MongoDB Integration**: Simplifies interactions with MongoDB databases.

---

## Validation Workflow

The validation process works as follows:

1. **Access Token Validation**: The primary step validates the access token.
2. **Fallback to X-API-KEY Validation**: If the access token validation fails, X-API-KEY validation is used.

**Note**: The JWKS should be in the format `List[Jwk_TH]`. Mention the symmetric or asymmetric algorithm you want to use :AUTH_TOKEN_ALGORITHM

```python
class Jwk_TH(TypedDict, total=False):
    alg: Required[str]
    e: str
    kid: Required[str]
    kty: str
    n: str
    use: str

def __load_jwks() -> List[Jwk_TH]:
    return json.loads(str(config("JWKS")))
```

---

## Configuration

Use an `.env` file to configure the library with the following keys:

```plaintext
ENVIRONMENT=develop
LOGGING_FILENAME=service.log
AUTH_TOKEN_ALGORITHM=RS256
BEDROCK_AWS_REGION_NAME=region_name
AWS_REGION_NAME=region_name
AWS_ACCESS_KEY_ID=amazing_access_key
AWS_SECRET_ACCESS_KEY=amazing_secret_access_key
X_API_KEY_EMBEDDING_SERVICE_1=access_key
X_API_KEY_EMBEDDING_SERVICE_2=access_key
AUTH_TOKEN_ALGORITHM=AUTH_TOKEN_ALGORITHM
JWKS=JWKS
```

---

## Example Code

### Headers Validation Model

The current headers validation model supports both inter-service calls and client-to-backend communication.
First it check cookie validation and then fallback to headers for authorization.

```python
import uuid
from pydantic import BaseModel, Field
from typing import Any, Dict

class Headers_PM(BaseModel):
    correlationid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str = "not_applicable"
    authorization: str = Field(default="")

    def model_dump(self, exclude_fields={}, **kwargs) -> Dict[str, Any]:
        return super().model_dump(**kwargs, exclude=exclude_fields)
```

### Setting up REST Middlewares

Below is an example of setting up REST middlewares in a FastAPI app:

```python
app.add_middleware(
    HeaderValidationMiddleware,
    x_api_key_1=cast(str, config("X_API_KEY_EMBEDDING_SERVICE_1")),
    x_api_key_2=cast(str, config("X_API_KEY_EMBEDDING_SERVICE_2")),
    authexpiryignore_paths=frozenset([
        ServicePaths.CONTEXT_PATH.value + "/encoders",
        ServicePaths.CONTEXT_PATH.value + "/llm",
    ]),
)
app.add_middleware(ExceptionMiddleware)
```

### Key Fields in `Headers_PM`

- **`correlationid`**: A unique identifier for tracing requests, generated using `uuid4()`.
- **`username`**: The username associated with the request; defaults to `"not_applicable"`.
- **`authorization`**: The authorization token, defaulting to an empty string.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

---

## PyPI Upload

To upload the library to PyPI, use the following steps:

```bash
pip install -r requirements.dev.txt
python setup.py bdist_wheel sdist
twine check dist/*
twine upload dist/*
```
