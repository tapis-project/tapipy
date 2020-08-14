# tapipy - Tapis V3 Python SDK

Python library for interacting with an instance of the Tapis API Framework.

## Development

This project is under active development, exploring different approaches to SDK generation.

## Installation

```
pip install tapipy
```

## Running the tests

Tests resources are contained within the `test` directory. `Dockerfile-tests` is at root.
1. Build the test docker image: `docker build -t tapis/tapipy-tests -f Dockerfile-tests .`
2. Run these tests using the built docker image: `docker run -it --rm  tapis/tapipy-tests`

## Usage

TODO - provide working examples, e.g., 
```
import tapipy
t = tapipy.Tapis(base_url='http://localhost:5001')
req = t.tokens.NewTokenRequest(token_type='service', token_tenant_id='dev', token_username='admin')
t.tokens.create_token(req)

import openapi_client
configuration = openapi_client.Configuration()
configuration.host = 'http://localhost:5001'
api_instance = openapi_client.TokensApi(openapi_client.ApiClient(configuration))

new_token = openapi_client.NewTokenRequest(token_type='service', token_tenant_id='dev', token_username='admin')

resp = api_instance.create_token(new_token)
jwt = resp.get('result').get('access_token').get('access_token')
```

## Build instructions

Building is done with poetry as follows:
```
pip install poetry
poetry install
```
This installs `tapipy` to a virtual environment. Run a shell in this environment with:
```
poetry shell
```

To install locally (not in a virtual environment):
```
pip install poetry
poetry build
cd dists
pip install *.whl
```

## PyPi Push Instructions

```
poetry build
poetry publish
```