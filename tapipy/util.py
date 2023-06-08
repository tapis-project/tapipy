from enum import Enum

class AttrDict(dict):
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

def tapisresult_to_json_serializer(result):
    if type(result) in [str, int, float, type(None), bool]: return result

    if type(result) == list:
        modified_result = []
        for res in result:
            modified_result.append(tapisresult_to_json_serializer(res))

        return modified_result

    modified_result = result.__dict__
    for prop in modified_result:
        modified_result[prop] = tapisresult_to_json_serializer(modified_result[prop])

    return modified_result

def dereference_spec(spec, new_spec=None):
    """
    Function to traverse through a Spec object, dereference $ref whenever it is encountered, 
    and store the dereferenced schema in a new dictionary.

    Note: The spec object is quite odd, it uses jsonschema-spec as it's library which is
    created by the same author as openapi_core. This uses / notation (overiding division)
    to traverse the spec object. Users have to `with spec.open() as k: print(k)` it to access
    dict it creates. The library lazy derefs, as in, it only derefs if you access the parent
    key of $ref. I'm not a huge fan, but this dereferences all $ref statements so we can 
    pickle and use the spec later.

    Parameters:
    spec (openapi_core.Spec): The Spec object.
    new_spec (dict, optional): The dictionary where the dereferenced schema will be stored. 
                               Defaults to None, in which case a new dictionary is created.

    Returns:
    dict: The new dictionary containing the dereferenced schema.
    """
    # If new_spec is not provided, initialize it as an empty dictionary
    if new_spec is None:
        new_spec = {}

    if isinstance(spec, dict):
        iter_spec = spec
    elif hasattr(spec, "__dict__"):
        iter_spec = vars(spec)
    else:
        iter_spec = spec

    for key, val in iter_spec.items():
        if key in  ["_resolver", "components"]:
            continue

        if isinstance(val, dict):
            new_spec[key] = {}
            dereference_spec(val, new_spec[key])

        # If the value at the current key is a list, create a new list in new_spec
        # and iterate over each item in the list
        elif isinstance(val, list):
            new_spec[key] = []
            for i, item in enumerate(val):
                # If the item is a dictionary, append a new dictionary to the list in new_spec
                # and recursively dereference the spec for the item
                if hasattr(item, "__dict__"):
                    new_spec[key].append({})
                    dereference_spec(val[i], new_spec[key][i])
                else:
                    new_spec[key].append(item)

        elif isinstance(val, Enum):
            new_spec[key] = val.name
            
        elif hasattr(val, "__dict__"):
            new_spec[key] = {}
            dereference_spec(val, new_spec[key])

        elif not hasattr(val, "__dict__"):
            new_spec[key] = val

    return new_spec