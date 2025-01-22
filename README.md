# PythonServiceUtil

PythonServiceUtil is a utility library designed for Python-based microservices. It provides seamless support for REST inter-service calls, AWS SQS, Redis, and MongoDB, enabling faster and more efficient microservice development.

## Features

- **REST Inter-service Calls**: Simplify HTTP requests between services.
- **AWS SQS Integration**: Streamline message queue operations.
- **Redis Support**: Efficient caching and data store capabilities.
- **MongoDB Integration**: Simplify database operations with MongoDB.


## PyPi Upload :

```bash
pip install -r  requirements.dev.txt
python setup.py bdist_wheel sdist
twine check dist/*
twine upload dist/*
```
