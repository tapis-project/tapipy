import time

from tapipy import errors
from tapipy.configuration import Config


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

def exponential_time(time_sec, retry_backoff_exponent=2):
    # If time_sec is 1, just double the time
    if time_sec == 1: return 2 
    return time_sec**retry_backoff_exponent

def constant_time(time_sec):
    return time_sec

# Wait the specified period of time then return the recalculated wait time
# according to the backoff alogrithm provided
def backoff(time_sec, algo="constant", exponent=2):
    backoff_recalculation_fn = constant_time
    kwargs = {}
    if algo == "constant" or algo == None:
        pass
    elif algo == "exponential":
        backoff_recalculation_fn = exponential_time
        kwargs["retry_backoff_exponent"] = exponent
    else:
        raise errors.TapyClientConfigurationError
    
    if time_sec > 0:
        time.sleep(time_sec)

    return backoff_recalculation_fn(time_sec, **kwargs)

# Decorator for Operation.__call__
# Retries operation __call__ n times after delay t secs on InternalServerError
# NOTE Only to be used on the __call__ function of an Operation instance
def retriable(op__call__):
    def wrapper(
        self, # Operation object
        *args,
        _config: Config=None,
        **kwargs
    ):
        config = self.tapis_client.config
        retries = config.retries if _config == None else _config.retries
        retry_delay_sec = config.retry_delay_sec if _config == None else _config.retry_delay_sec
        retry_on_exceptions = config.retry_on_exceptions if _config == None else _config.retry_on_exceptions
        retry_backoff_algo = config.retry_backoff_algo if _config == None else _config.retry_backoff_algo
        retry_backoff_exponent = config.retry_backoff_exponent if _config == None else _config.retry_backoff_exponent

        if type(retries) != int or retries < 0 :
            raise ValueError("Value provided to retry_delay_sec must be an integer and must be >= 0")
        
        exception = None
        while retries >= 0:
            try:
                return op__call__(self, *args, **kwargs)
            except Exception as e:
                exception = e
                if type(e) in retry_on_exceptions:
                    retries -= 1
                    # Wait the delay time, then recalculate delay time based on 
                    # backoff algorithm
                    retry_delay_sec = backoff(
                        retry_delay_sec,
                        algo=retry_backoff_algo,
                        exponent=retry_backoff_exponent
                    )
                    continue
                
                raise exception

        raise exception

    return wrapper