"""
Script to download/pickle/store configs under specified name.
This allows us to update the Tapipy configs with a script.
Note, this allows you to map any spec URL to any other URL filename as that's how they're saved.
MEANING! You can give an actor spec a 'files' filename and there will be no error, be careful.
"""

import os
import copy
import yaml
import requests
import pickle
from openapi_core import create_spec
from atomicwrites import atomic_write


###~~~#### FILL THESE IN ####~~~###
spec_dir = 'tapipy/specs'
resource_dir = 'tapipy/resources'
###################################


def get_file_info_from_url(url: str, spec_dir: str):
    """
    Using a url string we create a file name to store said url contents.
    """
    spec_name = url.replace('https://raw.githubusercontent.com/', '')\
                   .replace('.yml', '')\
                   .replace('.yaml', '')\
                   .replace('/', '-')\
                   .lower()
    full_spec_name = f'{spec_name}.pickle'
    spec_path = f'{spec_dir}/{spec_name}.pickle'
    return spec_name, full_spec_name, spec_path

def save_url_as_other_url(spec_and_alias, spec_dir):
    """
    Remember, filenames are derived from a URL, so you're essentially getting the data
    from one URL and giving it the URL of another. In most cases you can map URL1
    to URL1 and it'll act proper. But if a spec is broken, either use the existing or
    change the source URL.

    FOR EXAMPLE!
    The following line would cast the actors spec dict to the authenticators filename. This mean
    that Tapipy will ready in the actors spec when trying to get the authenticator url.
        spec_and_alias = {actor_master_url: authenticator_master_url}
    """

    for source_url, dest_url in spec_and_alias.items():
        # Get path from "dest_url". Where we'll save spec.
        _, _, dest_path = get_file_info_from_url(dest_url, spec_dir)

        if "local:" in source_url:
            # Loads yaml into Python dictionary
            try:
                source_path = source_url.replace('local:', '').strip()
                with open(source_path, 'rb') as spec_file:
                    spec_dict = yaml.load(spec_file, Loader=yaml.FullLoader)
            except Exception as e:
                print(f'Error reading local "{source_path}" resource. '
                      f'Ensure path is absolute. e:{e}')
                continue
            # Attempts to create spec from dict to ensure the spec is valid
            # We do a deepcopy as create_spec for some reason adds fields
            # to the dictionary that's given
            try:
                test_spec_dict = copy.deepcopy(spec_dict)
                create_spec(test_spec_dict)
            except Exception as e:
                print(f'Got exception when test creating spec for "{source_url}" '
                      f'resource; Spec probably not verifying; exception: {e}')
                continue
            # Pickles and saves the spec dict to the dest_path atomically
            try:
                with atomic_write(f'{dest_path}', overwrite=True, mode='wb') as spec_file:
                    pickle.dump(spec_dict, spec_file, protocol=4)
            except Exception as e:
                print(f'Got exception when attempting to pickle spec_dict and '
                      f'write to "{dest_path}"; exception: {e}')
                continue
        else:
            response = requests.get(source_url)
            if response.status_code == 200:
                # Loads yaml into Python dictionary
                try:
                    spec_dict = yaml.load(response.content, Loader=yaml.FullLoader)
                except Exception as e:
                    print(f'Got exception when attempting to load yaml from '
                          f'"{source_url}" resource; exception: {e}')
                    continue
                # Attempts to create spec from dict to ensure the spec is valid
                # We do a deepcopy as create_spec for some reason adds fields
                # to the dictionary that's given
                try:
                    test_spec_dict = copy.deepcopy(spec_dict)
                    create_spec(test_spec_dict)
                except Exception as e:
                    print(f'Got exception when test creating spec for "{source_url}" '
                          f'resource; Spec probably not verifying; exception: {e}')
                    continue
                # Pickles and saves the spec dict to the dest_path atomically
                try:
                    with atomic_write(f'{dest_path}', overwrite=True, mode='wb') as spec_file:
                        pickle.dump(spec_dict, spec_file, protocol=4)
                except Exception as e:
                    print(f'Got exception when attempting to pickle spec_dict and '
                        f'write to "{dest_path}"; exception: {e}')
                    continue

RESOURCES = {
    'local':{
        'actors': f"local: {resource_dir}/openapi_v3-actors.yml",
        'authenticator': f"local: {resource_dir}/openapi_v3-authenticator.yml",
        'meta': f"local: {resource_dir}/openapi_v3-meta.yml",
        'files': f"local: {resource_dir}/openapi_v3-files.yml",
        'sk': f"local: {resource_dir}/openapi_v3-sk.yml",
        'streams': f"local: {resource_dir}/openapi_v3-streams.yml",
        'systems': f"local: {resource_dir}/openapi_v3-systems.yml",
        'tenants': f"local: {resource_dir}/openapi_v3-tenants.yml",
        'tokens': f"local: {resource_dir}/openapi_v3-tokens.yml",
    },
    'tapipy':{
        'actors': 'https://raw.githubusercontent.com/tapis-project/tapipy/prod/tapipy/resources/openapi_v3-actors.yml',
        'authenticator': 'https://raw.githubusercontent.com/tapis-project/tapipy/prod/tapipy/resources/openapi_v3-authenticator.yml',
        'meta': 'https://raw.githubusercontent.com/tapis-project/tapipy/prod/tapipy/resources/openapi_v3-meta.yml',
        'files': 'https://raw.githubusercontent.com/tapis-project/tapipy/prod/tapipy/resources/openapi_v3-files.yml',
        'sk': 'https://raw.githubusercontent.com/tapis-project/tapipy/prod/tapipy/resources/openapi_v3-sk.yml',
        'streams': 'https://raw.githubusercontent.com/tapis-project/tapipy/prod/tapipy/resources/openapi_v3-streams.yml',
        'systems': 'https://raw.githubusercontent.com/tapis-project/tapipy/prod/tapipy/resources/openapi_v3-systems.yml',
        'tenants': 'https://raw.githubusercontent.com/tapis-project/tapipy/prod/tapipy/resources/openapi_v3-tenants.yml',
        'tokens': 'https://raw.githubusercontent.com/tapis-project/tapipy/prod/tapipy/resources/openapi_v3-tokens.yml'
    },
    'prod': {
        'actors': 'https://raw.githubusercontent.com/TACC/abaco/dev-v3/docs/specs/openapi_v3.yml',               
        'authenticator': 'https://raw.githubusercontent.com/tapis-project/authenticator/prod/service/resources/openapi_v3.yml',
        'meta': 'https://raw.githubusercontent.com/tapis-project/tapis-client-java/prod/meta-client/src/main/resources/metav3-openapi.yaml',
        'files': 'https://raw.githubusercontent.com/tapis-project/tapis-files/prod/api/src/main/resources/openapi.yaml',
        'sk': 'https://raw.githubusercontent.com/tapis-project/tapis-client-java/prod/security-client/src/main/resources/SKAuthorizationAPI.yaml',
        'streams': 'https://raw.githubusercontent.com/tapis-project/streams-api/prod/service/resources/openapi_v3.yml',
        'systems': 'https://raw.githubusercontent.com/tapis-project/openapi-systems/prod/SystemsAPI.yaml',
        'tenants': 'https://raw.githubusercontent.com/tapis-project/tenants-api/prod/service/resources/openapi_v3.yml',
        'tokens': 'https://raw.githubusercontent.com/tapis-project/tokens-api/prod/service/resources/openapi_v3.yml'
    },
    'dev': {
        'actors': 'https://raw.githubusercontent.com/TACC/abaco/dev-v3/docs/specs/openapi_v3.yml',
        'authenticator': 'https://raw.githubusercontent.com/tapis-project/authenticator/dev/service/resources/openapi_v3.yml',
        'meta': 'https://raw.githubusercontent.com/tapis-project/tapis-client-java/dev/meta-client/src/main/resources/metav3-openapi.yaml',
        'files': 'https://raw.githubusercontent.com/tapis-project/tapis-files/dev/api/src/main/resources/openapi.yaml',
        'sk': 'https://raw.githubusercontent.com/tapis-project/tapis-client-java/dev/security-client/src/main/resources/SKAuthorizationAPI.yaml',
        'streams': 'https://raw.githubusercontent.com/tapis-project/streams-api/dev/service/resources/openapi_v3.yml',
        'systems': 'https://raw.githubusercontent.com/tapis-project/openapi-systems/dev/SystemsAPI.yaml',
        'tenants': 'https://raw.githubusercontent.com/tapis-project/tenants-api/dev/service/resources/openapi_v3.yml',
        'tokens': 'https://raw.githubusercontent.com/tapis-project/tokens-api/dev/service/resources/openapi_v3.yml'
    }
}

# Spec/Key is the url to download and copy the spec dict from.
# Alias/Val is the file to save the spec dict to.

spec_and_alias = {'source_spec_url': 'destination_spec_url'}

# Set 1 updates all tapipy pickle files with the local specs held in the resources folder.
spec_and_alias_set_1 = {RESOURCES['local']['actors']: RESOURCES['tapipy']['actors'],
                        RESOURCES['local']['authenticator']: RESOURCES['tapipy']['authenticator'],
                        RESOURCES['local']['meta']: RESOURCES['tapipy']['meta'],
                        RESOURCES['local']['files']: RESOURCES['tapipy']['files'],
                        RESOURCES['local']['sk']: RESOURCES['tapipy']['sk'],
                        RESOURCES['local']['streams']: RESOURCES['tapipy']['streams'],
                        RESOURCES['local']['systems']: RESOURCES['tapipy']['systems'],
                        RESOURCES['local']['tenants']: RESOURCES['tapipy']['tenants'],
                        RESOURCES['local']['tokens']: RESOURCES['tapipy']['tokens']}

# Set 2 updates all tapipy pickle files with the specs contained
# in each specs source's prod branch. So updating them completely.
spec_and_alias_set_2 = {RESOURCES['prod']['actors']: RESOURCES['tapipy']['actors'],
                        RESOURCES['prod']['authenticator']: RESOURCES['tapipy']['authenticator'],
                        RESOURCES['prod']['meta']: RESOURCES['tapipy']['meta'],
                        RESOURCES['prod']['files']: RESOURCES['tapipy']['files'],
                        RESOURCES['prod']['sk']: RESOURCES['tapipy']['sk'],
                        RESOURCES['prod']['streams']: RESOURCES['tapipy']['streams'],
                        RESOURCES['prod']['systems']: RESOURCES['tapipy']['systems'],
                        RESOURCES['prod']['tenants']: RESOURCES['tapipy']['tenants'],
                        RESOURCES['prod']['tokens']: RESOURCES['tapipy']['tokens']}
 
# Specify where you want the specs to be saved, to get ready for a release
# specify the github/tapipy/tapipy/specs folder to overwrite old specs.
# Don't forget to delete any specs that are no longer needed.

# Run the saver
save_url_as_other_url(spec_and_alias_set_1, spec_dir)
