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

    # Open the Spec object and store the result in spec_obj
    with spec.open() as k:
        spec_obj = k

    # Iterate over all keys in spec_obj
    for key, _ in spec_obj.items():
        next_val = spec_obj[key]

        # If the value at the current key is a dictionary, create a new dictionary in new_spec
        # and recursively dereference the spec at the current key
        if isinstance(next_val, dict):
            new_spec[key] = {}
            dereference_spec(spec / key, new_spec[key])

        # If the value at the current key is a list, create a new list in new_spec
        # and iterate over each item in the list
        elif isinstance(next_val, list):
            new_spec[key] = []
            for i, item in enumerate(next_val):
                # If the item is a dictionary, append a new dictionary to the list in new_spec
                # and recursively dereference the spec for the item
                if isinstance(item, dict):
                    new_spec[key].append({})
                    dereference_spec(spec / key / i, new_spec[key][i])
                # If the item is not a dictionary, append it directly to the list in new_spec
                else:
                    new_spec[key].append(item)
        # If the value at the current key is neither a dictionary nor a list,
        # copy it directly to new_spec
        else:
            new_spec[key] = spec_obj[key]

    # Return the new dictionary containing the dereferenced schema
    return new_spec