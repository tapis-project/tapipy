import datetime
import json
import os

from tapipy.tapis import Tapis

__all__ = ['TapisLocalCache']

DEFAULT_CACHE_FILE = 'client.json'


class TapisLocalCache(Tapis):
    """A client for the Tapis API that caches client and token in a local file
    """
    def __init__(self, cache_dir=None, cache=None, **kwargs):
        setattr(self, 'user_tokens_cache_path',
                self.path_to_cache(cache_dir, cache))
        super().__init__(**kwargs)

    @classmethod
    def path_to_cache(cls, cache_dir=None, cache=None):
        # Cache directory resolves as:
        # 1. Provided value 2. TAPIS3_CACHE_DIR 3. ~/.tapis3
        if cache_dir is None:
            cache_dir = os.environ.get('TAPIS3_CACHE_DIR',
                                       os.path.expanduser('~/.tapis3'))
        if cache is None:
            cache = DEFAULT_CACHE_FILE
        return os.path.join(cache_dir, cache)

    @classmethod
    def restore(cls, cache_dir=None, cache=None):
        """Load Tapis client from cached credentials
        """
        cache_path = cls.path_to_cache(cache_dir, cache)
        with open(cache_path, 'r') as cl:
            data = json.load(cl)
            t = TapisLocalCache(base_url=data['base_url'],
                                tenant_id=data['tenant_id'],
                                access_token=data['access_token'],
                                refresh_token=data['refresh_token'],
                                client_id=data['client_id'],
                                client_key=data['client_key'],
                                verify=True)
            return t

    def refresh_user_tokens(self):
        """Refresh access and refresh tokens, then save to cache
        """
        class DateTimeEncoder(json.JSONEncoder):
            #Override the default method
            def default(self, obj):
                if isinstance(obj, (datetime.date, datetime.datetime)):
                    return obj.isoformat()

        resp = super().refresh_user_tokens()

        # Not sure we need to do these checks...
        if isinstance(self.access_token, str):
            access_token = self.access_token
            expires_at = None
        else:
            access_token = self.access_token.access_token
            expires_at = self.access_token.expires_at
        if isinstance(self.access_token, str):
            refresh_token = self.refresh_token
        else:
            refresh_token = self.refresh_token.refresh_token

        data = {
            'base_url': self.base_url,
            'tenant_id': self.tenant_id,
            'client_id': self.client_id,
            'client_key': self.client_key,
            'access_token': access_token,
            'refresh_token': refresh_token,
            # The expires_at key is not used by Tapis but is here
            # as a debug aid so one can quickly tell when a token
            # pair is _expected_ to expire
            'expires_at': expires_at
        }

        # Wrap in a try block in case writing fails. This supports use of
        # TapisLocalCache inside a read-only environment such as a container
        try:
            cache_dir = os.path.dirname(self.user_tokens_cache_path)
            if not os.path.isdir(cache_dir):
                os.makedirs(cache_dir, exist_ok=True)
            with open(self.user_tokens_cache_path, 'w') as cl:
                json.dump(data, cl, cls=DateTimeEncoder, indent=4)
        except Exception as exc:
            warnings.warn('Failed to write to cache file: {0}'.format(exc))

        return resp
