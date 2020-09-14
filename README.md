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

## Important Parameters to Know

The Tapipy package allows for spec file customization in Tapis object initialization:
* resource_set: str 
	* Determines which set of resource to use, master or dev, defaults to master.
	* Important to note that if a custom_spec_dictionary is used, it is appended to this resource_set.
		* For example, you would set master and then specify a custom specs that will be added on.
* custom_spec_dict: {resource_name: str, resource_url: str}
	* Allows users to modify the base resource set urls.
		* e.g. I can specify actor as a resource name and change the url.
	* Also allows users to add new resources to the set.
		* e.g. I can add a new resource named "test" with a  custom url.
		* Important that know that any new specs will be downloaded and added to the cache
			* No need to specify download_latest_specs or update spec files.
* download_latest_specs: bool
	* Allows users to re-download all specs regardless on if they already exist in the cache. Defaulted to False
	* This will happen every time the Tapis object is initialized, it's a tad slower, and can cause live updates to specs.
		* As such, be warned. There are functions to update spec files below.
* spec_dir: str
	* Allows users to specify folder to save specs to. Defaults to none which uses Tapipy's package folder.
	* If you are updating specs it's wise to use a different folder in order to not modify the base specs.

The following is an example of some custom parameter setting. As you can see, the abaco resource will now use the spec at `URL#1`, overwriting the resource definition in the master resource set, it'll download it if it doesn't exist. The same for the longhorn resource. This means that the Tapis object will now have access to all specs in master like normal, but with a modified abaco and with a new longhorn resource. All of these are stored at the new spec_dir because I don't want to accidentally overwrite any base specs if I call `update_spec_cache()` later (talked about in the next section).
```
from tapipy.tapis import Tapis

t = Tapis(base_url='https://master.develop.tapis.io',
          tenant_id='master',
          username='username',
          account_type='user',
          password='password',
          resource_set='master',
          custom_spec_dict={'abaco': 'URL#1',
                            'longhorn': 'URL#2'},
          spec_dir='/home/username/tapipy_specs')
t.get_tokens()
```

## Update Specs Files

The Tapipy package now uses a cache to organize spec dictionaries as pickled files and has the ability to accept custom spec files. By default Tapipy keeps a set of base spec files in the `%tapipy%/specs` folder. These specs are pre-pickled at package creation time.

In order to update all default spec files a user can use the `update_spec_cache()` function. Said function's definition is below. If no resources are provided the function will download all default spec urls in the RESOURCES object in `%tapipy%/tapipy/tapis.py` file.
```
Resources = Dict[ResourceName, ResourceUrl]
update_spec_cache(resources: Resources = None, spec_dir: str = None)
```
Users are able to specify custom resources to download by providing their own resource dictionary. For example, providing `{'actors': 'URLToMyActorDictionary'}` would update that spec.

Users can also specify here where to update the spec with the `spec_dir` variable.

The Tapis object itself also has a `update_spec_cache()` function that takes the Tapis parameters given at startup and updates the spec cache. Meaning that if the Tapis object was given a custom dictionary, the `update_spec_cache()` function would update it without the need for setting parameters.
```
t.update_spec_cache()
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