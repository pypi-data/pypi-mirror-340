![CrowdStrike Falcon](https://raw.githubusercontent.com/CrowdStrike/foundry-fn-python/main/docs/asset/cs-logo.png)

# Falcon Foundry Function as a Service Python SDK

`falcon-foundry-python` is a community-driven, open source project designed to enable the authoring of functions.
While not a formal CrowdStrike product, `falcon-foundry-python` is maintained by CrowdStrike and supported in partnership
with the open source developer community.

## Installation ⚙️

### Via `pip`

The SDK can be installed or updated via `pip install`:

```shell
python3 -m pip install crowdstrike-falcon-foundry
```

## Quickstart 💫

### Code

Add the SDK to your project by following the [installation](#installation) instructions above,
then create your `handler.py`:

```python
import logging
from falconfoundry import (
    FoundryAPIError,
    FoundryRequest,
    FoundryResponse,
    FoundryFunction,
)

func = FoundryFunction.instance()  # *** (1) ***


@func.handler(method='POST', path='/create')  # *** (2) ***
def on_create(request: FoundryRequest, config: [dict[str, any], None],
              logger: logging.Logger) -> FoundryResponse:  # *** (3), (4), (5) ***
    if len(request.body) == 0:
        return FoundryResponse(
            code=400,
            errors=[FoundryAPIError(code=400, message='empty body')]
        )

    #####
    # do something useful
    #####

    return FoundryResponse(  # *** (6) ***
        body={'hello': 'world'},
        code=200,
    )


@func.handler(method='PUT', path='/update')
def on_update(request: FoundryRequest) -> FoundryResponse:  # *** (7) ***
    # do stuff
    return FoundryResponse(
        # ...snip...
    )


@func.handler(method='DELETE', path='/foo')
def on_delete(request: FoundryRequest, config: [dict[str, any], None]) -> FoundryResponse:  # *** (8) ***
    # do stuff
    return FoundryResponse(
        # ...snip...
    )


if __name__ == '__main__':
    func.run()  # *** (9) ***
```

1. `FoundryFunction`: The `FoundryFunction` class wraps the Foundry Function implementation.
   Each `FoundryFunction` instance consists of a number of handlers, with each handler corresponding to an endpoint.
   Only one `FoundryFunction` should exist per Python implementation.
   Multiple `FoundryFunction`s will result in undefined behavior.
2. `@func.handler`: The handler decorator defines a Python function/method as an endpoint.
   At a minimum, the `handler` must have a `method` and a `path`.
   The `method` must be one of `DELETE`, `GET`, `PATCH`, `POST`, and `PUT`.
   The `path` corresponds to the `url` field in the request.
   The SDK will provide any loaded configuration as an argument.
3. Methods decorated with `@handler` must take arguments in the order of `FoundryRequest` and `dict|None`
   (i.e. the request and either the configuration or nothing; see example above),
   and must return a `FoundryResponse`.
4. `request`: FoundryRequest payload and metadata. At the time of this writing, the `FoundryRequest` object consists of:
    1. `body`: The request payload as given in the Function Gateway `body` payload field. Will be deserialized as
       a `dict[str, Any]`.
    2. `params`: Contains request headers and query parameters.
    3. `url`: The request path relative to the function as a string.
    4. `method`: The request HTTP method or verb.
    5. `access_token`: Caller-supplied access token.
5. `logger`: Unless there is specific reason not to, the function author should use the `Logger` provided to the
   function.
   When deployed, the supplied `Logger` will be formatted in a custom manner and will have fields injected to assist
   with working against our internal logging infrastructure.
   Failure to use the provided `Logger` can thus make triage more difficult.
6. Return from a `@handler` function: Returns a `FoundryResponse` object.
   The `FoundryResponse` object contains fields `body` (payload of the response as a `dict`),
   `code` (an `int` representing an HTTP status code),
   `errors` (a list of any `FoundryAPIError`s), and `header` (a `dict[str, list[str]]` of any special HTTP headers which
   should be present on the response).
   If no `code` is provided but a list of `errors` is, the `code` will be derived from the greatest positive valid HTTP
   code present on the given `FoundryAPIError`s.
7. `on_update(request: FoundryRequest)`: If only one argument is provided, only a `FoundryRequest` will be provided.
8. `on_delete(request: FoundryRequest, config: [dict[str, any], None])`: If two arguments are provided, a `FoundryRequest` and config
   will be provided.
9. `func.run()`: Runner method and general starting point of execution.
   Calling `run()` causes the `FoundryFunction` to finish initializing and start executing.
   Any code declared following this method may not necessarily be executed.
   As such, it is recommended to place this as the last line of your script.

### Testing locally

The SDK provides an out-of-the-box runtime for executing the function.
A basic HTTP server will be listening on port 8081.

```shell
cd my-project && python3 main.py
```

Requests can now be made against the executable.

```shell
curl -X POST 'http://localhost:8081' \
  -H 'Content-Type: application/json' \
  --data '{
    "body": {
        "foo": "bar"
    },
    "method": "POST",
    "url": "/create"
}'
```

## Working with `falconpy`

Foundry function authors should import `falconpy` explicitly as a requirement in their project when needed.

### General usage

**Important:** Create a new instance of each `falconpy` client you want on each request.

```python
# omitting other imports
from falconpy.alerts import Alerts
from falconfoundry import cloud, FoundryFunction

func = FoundryFunction.instance()


@func.handler(...)
def endpoint(request):
    # ... omitting other code ...
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!! create a new client instance on each request !!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    falconpy_alerts = Alerts(access_token=request.access_token, base_url=cloud())

    # ... omitting other code ...
```

---


<p align="center"><img src="https://raw.githubusercontent.com/CrowdStrike/foundry-fn-python/main/docs/asset/cs-logo-footer.png"><BR/><img width="250px" src="https://raw.githubusercontent.com/CrowdStrike/foundry-fn-python/main/docs/asset/adversary-red-eyes.png"></P>
<h3><P align="center">WE STOP BREACHES</P></h3>
