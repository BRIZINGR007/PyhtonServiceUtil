# PythonServiceUtil

**PythonServiceUtil** is a utility library designed to streamline Python-based microservice development. It offers robust support for:

- **REST Inter-service Calls**: Simplifies HTTP communication between services.
- **AWS SQS Integration**: Enhances message queue operations.
- **Redis Support**: Provides efficient caching and data storage.
- **MongoDB Integration**: Simplifies database interactions, including transactions (mongoengine object data mapper).
- **Context Management**: Facilitates seamless context management in multithreaded and multiprocessing environments.

---

## Features

### Validation Workflow

The validation process is structured as follows:

1. **Access Token Validation**: Validates the access token as the primary step.
2. **Fallback to X-API-KEY Validation**: If the access token validation fails, X-API-KEY validation is used as a fallback.

> **Note**: The JWKS (JSON Web Key Set) must follow the format `List[Jwk_TH]`. Specify the symmetric or asymmetric algorithm to use via `AUTH_TOKEN_ALGORITHM`.

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

Configure the library using an `.env` file with the following keys:

```plaintext
ENVIRONMENT=develop
LOGGING_FILENAME=service.log
AUTH_TOKEN_ALGORITHM=RS256
BEDROCK_AWS_REGION_NAME=region_name
AWS_REGION_NAME=region_name
AWS_ACCESS_KEY=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_access_key
X_API_KEY_EMBEDDING_SERVICE_1=access_key
X_API_KEY_EMBEDDING_SERVICE_2=access_key
JWKS=JWKS
```

---

## Usage

### Headers Validation Model

The headers validation model supports both inter-service calls and client-to-backend communication. It first checks cookie validation and then falls back to header-based authorization.

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

### Setting Up REST Middlewares

Here is an example of setting up REST middlewares in a FastAPI app:

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

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

---

## Publishing to PyPI

To upload the library to PyPI, follow these steps:

```bash
pip install -r requirements.dev.txt
python setup.py bdist_wheel sdist
twine check dist/*
twine upload dist/*
```
