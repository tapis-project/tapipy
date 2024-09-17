from tapipy.util import retriable
from tapipy.configuration import Config


class TapisClientMock:
    def __init__(self, config: Config=None):
        self.config = Config() if config == None else config

class OperationMock:
    def __init__(self, raises=None, succeeds_on_nth_retry=None, result=None, config: Config=None):
        self.tapis_client = TapisClientMock(config=config)
        self._raises = raises
        self._succeeds_on_nth_retry=succeeds_on_nth_retry
        self._result = result
        self.times_called = 0
        self.times_retried = 0
        self.args = []
        self.kwargs = {}

    @retriable
    def __call__(self, *args, **kwargs):
        self.args = (self, *args)
        self.kwargs = kwargs
        if self.times_called >= 1:
            self.times_retried += 1
        self.times_called += 1

        if (
            self._succeeds_on_nth_retry != None
            and self._succeeds_on_nth_retry == self.times_retried
        ):
            return self._result

        raise_error = self._raises != None
        if raise_error:
            raise self._raises()
        
        return self._result
