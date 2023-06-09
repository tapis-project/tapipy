"""
This script polls all resources in the "RESOURCES['prod']" dict from tapipy.
This dict has urls to all specs it needs in prod. We use the github api
to get each file once.

These api.github.com gets have an "ETag" returned with headers; subsequent
polling to api.github.com where we include the returned ETag value
as a header will only return a '200' status code when the data is modified.
So if we save a dict with said ETags and always call api.github.com with them,
we get a "free" check on whether or not the file was modified since the last
time we polled it.
"""
import os
import sys
import json
import yaml
import copy
import base64
import requests as r
from openapi_core import Spec
# Get spec urls to check.
from repo_spec_creation_script import RESOURCES
from tapipy.util import dereference_spec

resourceFolderPath='tapipy/resources/'
etagsFileName='resource_etags.json'
etagsFilePath = f'{resourceFolderPath}/{etagsFileName}'

if os.path.isfile(etagsFilePath):
    with open(etagsFilePath, 'r') as f:
        etagsDict = json.load(f)
else:
    etagsDict = {}

newSpecs = []

print(f'Dealing with specs now')
for specKey, specUrl in RESOURCES['prod'].items():
    # url follows 'https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}' format.
    if '/prod/' in specUrl:
        specUrl = specUrl.replace('/prod/', '/contents/')
        specUrl = f"{specUrl}?ref=prod"
    elif '/dev-v3/' in specUrl:
        specUrl = specUrl.replace('/dev-v3/', '/contents/')
        specUrl = f"{specUrl}?ref=dev-v3"
    elif '/prod-v3/' in specUrl:
        specUrl = specUrl.replace('/prod-v3/', '/contents/')
        specUrl = f"{specUrl}?ref=prod-v3"

    url = specUrl.replace('raw.githubusercontent.com', 'api.github.com/repos')
    print(f'\n\n"{specKey}" resource url: {url}')
    if specKey in etagsDict:
        res = r.get(url,
                    headers={'If-None-Match': etagsDict[specKey]})
    else:
        res = r.get(url)
    if not res.status_code in [200, 304]:
        raise Exception(f'Unexpected response status code for url: {url}; Issue: {res.status_code} - {res.content}')
    if res.status_code == 200:
        print(f'Got new spec for "{specKey}" resource.')
        retrieved_spec = base64.b64decode(res.json()['content']).decode('utf-8')
        try:
            # Directly creates spec from response. This validates spec as valid.
            spec = Spec.from_file(retrieved_spec)
        except Exception as e:
            print(f'Got exception when attempting to load create spec for '
                  f'"{specKey}" resource; exception: {e}')
            continue
        try:
            # Dereference spec so we have a dict we can pickle.
            spec_dict = dereference_spec(spec)
        except Exception as e:
            print(f'Got exception when derefrencing spec for "{specKey}" '
                    f'resource; Spec probably not verifying; exception: {e}')
            continue

        try:
            with open(f'{resourceFolderPath}/openapi_v3-{specKey}.yml', 'w') as f:
                f.write(retrieved_spec)
            etagsDict[specKey] = res.headers['ETag']
            newSpecs.append(specKey)
        except FileNotFoundError:
            raise FileNotFoundError(f'Please ensure the resources folder specified exists: {resourceFolderPath}')
        except Exception as e:
            raise Exception(f'Got exception writing spec to resources folder: {e}')
    else:
        print(f'No new spec for "{specKey}" resource.')

try:
    with open(etagsFilePath, 'w') as f:
        json.dump(etagsDict, f)
except Exception as e:
    raise Exception("Got exception writing to ETags json file.")

try:
    if newSpecs:
        commit_message = f'Jenkins: Updating specs for {", ".join(newSpecs)}.'
        with open('commit_message.txt', 'w') as f:
            f.write(commit_message)
except Exception as e:
    raise Exception("Got exception writing to ETags json file.")
