# FastAPI

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints. FastAPI is designed to be easy to use, fast to code, and easy to learn while offering automatic interactive documentation.

## Features

- Fast: Very high performance, on par with NodeJS and Go (thanks to Starlette and Pydantic).
- Fast to code: Increase the speed to develop features by about 200% to 300%.
- Fewer bugs: Reduce about 40% of human (developer) induced errors.
- Easy: Designed to be easy to use and learn.
- Automatic interactive documentation: Swagger UI and ReDoc (using OpenAPI).
- Based on standards: Based on (and fully compatible with) OpenAPI and JSON Schema.
- Pythonic: Designed for Python 3.6+ with Python type hints.

## Installation

To install FastAPI, you can use `pip`:

```bash
pip install fastapi
```

## Usage

To create a FastAPI application, you can use the `FastAPI` class:

```python
from fastapi import FastAPI

app = FastAPI()
```

## Running the application

To run the application, you can use the `uvicorn` server:

```bash
uvicorn app.main:app --reload
```

## Documentation

To access the interactive documentation, you can use the following URL:

```
http://127.0.0.1:8000/docs
```

## Testing

To test the application, you can use the following command:

```bash
pytest
```