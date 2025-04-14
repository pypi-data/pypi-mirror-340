# WrAPIpy

WrAPIpy provides:

- a Pythonic wrapper `wrapipy.WrAPIpy` around a Swagger 2.0 API documentation object that allows to conveniently send requests to the API's endpoints and receive their responses,
- and a Pydantic specification of the documentation object, `wrapipy.SwaggerDoc`, which is a relaxed model of Swagger 2.0 directly parseable using the build-in `json` library.

## Basic Usage

### Parse a Swagger JSON File

```python
from wrapipy import SwaggerDoc
import json

with open("path_to_swagger", "r") as f:
    data = json.load(f)
swagger = SwaggerDoc(**data)
```

### Send Requests to an API

```python
from wrapipy import WrAPI

api = WrAPI(swagger)
r = api.request(
    "endpoint_path", 
    {
        "query": {
            # query params here as key-value dicts
        },
        "path": "path_param",
        "payload": {
            # payload params here as key-value dicts
        }
    }
)
```

### Full Example

```python
from wrapipy import SwaggerDoc, WrAPI
import json

with open("path_to_swagger", "r") as f:
    data = json.load(f)
swagger = SwaggerDoc(**data)
api = WrAPI(swagger)
r = api.request(
    "endpoint_path", 
    {
        "query": {
            # query params here as key-value dicts
        },
        "path": "path_param",
        "payload": {
            # payload params here as key-value dicts
        }
    }
)
```

### Make a Swagger-like Documentation

Sometimes the API you wish to connec to does not have a Swagger documentation or has a lot more endpoints than the ones you need. In that case, you can create a Swagger-like documentation using Python dictionaries. The minimal working example follows, but any other Swagger 2.0 supported fields can be provided.

```python
from wrapipy import WrAPI, SwaggerDoc

data = {
    "paths": {
        "/my/path": {
            "parameters": [],
            "get":{
                "responses":{
                    "200": {}
                }
            }
        }
    }
}
swagger = SwaggerDoc(**data)
wrapi = WrAPI(swagger)
```

A full API documentation is available at [wrapi-documentation.onrender.com](https://wrapi-documentation.onrender.com).

## Advanced Options: Resend Requests

The `request` method of `wrapipy.WrAPI` allows to specify an additional parameter `retry_responses` (default `[429]`). When a response from this list of response codes is received, it resend the request after `wait_time` seconds (default `0.1`) until a different response is received or until there have been `max_attempts` attempts (default `100`).

---

This project was initialised with [Cookiecutter](https://github.com/audreyr/cookiecutter).
