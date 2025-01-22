# PythonServiceUtil

PythonServiceUtil is a utility library designed for Python-based microservices. It provides seamless support for REST inter-service calls, AWS SQS, Redis, and MongoDB, enabling faster and more efficient microservice development.

## Features

- **REST Inter-service Calls**: Simplify HTTP requests between services.
- **AWS SQS Integration**: Streamline message queue operations.
- **Redis Support**: Efficient caching and data store capabilities.
- **MongoDB Integration**: Simplify database operations with MongoDB.

---

## Configuration

To configure the library, use an `.env` file with the following keys:

```plaintext
ENVIRONMENT=develop
BEDROCK_AWS_REGION_NAME=region_name
AWS_REGION_NAME=region_name
AWS_ACCESS_KEY_ID=amazing_access_key
AWS_SECRET_ACCESS_KEY=amazing_secret_access_key
```

---

## Example Code

Below is teh current headers  validation Model both for message context as well as for  interservice call or  client  to backend call.

The rest  middleware support both validation of  auth  token both from cookie or from headers . 

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

### Explanation

- **`correlationid`**: A unique identifier for tracing requests, generated using `uuid4()`.
- **`username`**: The username associated with the request; defaults to "not_applicable".
- **`authorization`**: The authorization token, defaulting to an empty string.
- **`model_dump`**: A method for exporting the model as a dictionary, with optional field exclusion.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contributing

Contributions are welcome! Please follow the steps below:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

---

## PyPi Upload :

```bash
pip install -r  requirements.dev.txt
python setup.py bdist_wheel sdist
twine check dist/*
twine upload dist/*
```
