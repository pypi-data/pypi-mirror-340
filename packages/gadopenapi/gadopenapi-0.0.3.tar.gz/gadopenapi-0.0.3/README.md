<p align="center">
  <a href="https://github.com/AlexDemure/gadopenapi">
    <a href="https://ibb.co/6cqwTKh6"><img src="https://i.ibb.co/zWtxB3cK/logo.png" alt="logo" border="0"></a>
  </a>
</p>

<p align="center">
  Utility toolkit to modify and override OpenAPI schema definitions in FastAPI.
</p>

---

## Installation

```
pip install gadopenapi
```

## Usage
```
from gadopenapi import OpenAPI

app.openapi = OpenAPI(app)

# or

@app.get("/api/openapi.json", include_in_schema=False)
async def openapi():
    return OpenAPI(app, handlers=[affix, use_route_as_operation_id]).generate()
```

### Extension ```gadopenapi.extensions.affix```

```
from fastapi import FastAPI
from pydantic import BaseModel

from gadopenapi import OpenAPI
from gadopenapi.extensions.affix import affix

app = FastAPI()

app.openapi = OpenAPI(app, handlers=[affix])


class Deprecated(BaseModel):
    __affix__ = "Deprecated:"


class User(Deprecated):
    id: int


@app.get("/user", response_model=User)
def get_user():
    return {"id": 1}

openapi.json
>>>
{
  "paths": {
    "schema": {
      "$ref": "#/components/schemas/DeprecatedUser"
    }
  },
  "schemas": {
      "DeprecatedUser": {
        "title": "DeprecatedUser"
      }
    }
}
```

### Extension ```gadopenapi.extensions.operationid```

```
from fastapi import FastAPI
from pydantic import BaseModel

from gadopenapi import OpenAPI
from gadopenapi.extensions.operationid import use_route_as_operation_id

app = FastAPI()

app.openapi = OpenAPI(app, handlers=[use_route_as_operation_id])


class User(BaseModel):
    id: int


@app.get("/user", response_model=User)
def get_user():
    return {"id": 1}

openapi.json
>>> BEFORE
{
  "paths": {
    "/user": {
      "get": {
        "operationId": "get_user_user_get",
      }
    }
  }
}

>>> AFTER
{
  "paths": {
    "/user": {
      "get": {
        "operationId": "get_user",
      }
    }
  }
}
```

### Extension ```gadopenapi.extensions.errors``` 

```
from fastapi import FastAPI
from gadopenapi.extensions.errors import APIError, openapi_errors

app = FastAPI()


class MyError(APIError):
    ...


@app.get("/user", response_model=dict, responses=openapi_errors(MyError))
def get_user():
    return {"id": 1}

openapi.json
>>>
{
  "paths": {
    "/user": {
      "get": {
        "responses": {
          "200": {
            "description": "Successful Response"
          },
          "418": {
            "description": "MyError",
            "content": {
              "application/json": {
                "example": {
                  "status_code": 418,
                  "detail": {
                    "type": "MyError"
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```


### Custom handler

```
from fastapi import FastAPI
from gadopenapi import OpenAPI

def my_handler(app: FastAPI, openapi: dict) -> tuple[FastAPI, dict]:
    # Mutate openapi here
    return app, openapi

app = FastAPI()

app.openapi = OpenAPI(app, handlers=[my_handler])

@app.get("/user", response_model=dict)
def get_user():
    return {"id": 1}
```
