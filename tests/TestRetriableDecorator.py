import unittest

from .mocks import RetriableMock
from tapipy.errors import InternalServerError


class TestRetriableDecorator(unittest.TestCase):
    def testRetriableCallsOnce(self):
        # # NOTE Retriable decorator can be found on the __call__ method of the
        # RetriableMock
        mock = RetriableMock()
        mock()
        assert mock.times_called == 1
        assert mock.times_retried == 0

    def testRetriableMisconfigured(self):
        mock = RetriableMock()
        self.assertRaises(ValueError, mock, _retries=1.5) # Only integers
        self.assertRaises(ValueError, mock, _retries=-1) # Must be >= 0
    
    def testRetriableRaisesSpecifedExceptionWhichOverridesDefault(self):
        _ = RetriableMock(
            raises=InternalServerError,
            succeeds_on_nth_retry=None # Fails forever
        )
        mock2 = RetriableMock(
            raises=TypeError,
            succeeds_on_nth_retry=None # Fails forever
        )
        self.assertRaises(
            TypeError,
            mock2,
            _retries=3,
            _retry_on_exceptions=[TypeError]
        )
        
    def testRetriableRetriesUnitilRetryLimitReached(self):
        mock = RetriableMock(
            raises=InternalServerError,
            succeeds_on_nth_retry=None # Fails forever
        )
        self.assertRaises(
            InternalServerError,
            mock,
            _retries=3,
            _retry_on_exceptions=[InternalServerError]
        )
        assert mock.times_called == 4
        assert mock.times_retried == 3

    def testRetriableSuccedsBeforeReachingRetryLimit(self):
        mock = RetriableMock(
            raises=InternalServerError,
            succeeds_on_nth_retry=2,
            result=1337
        )
        result = mock(
            _retries=3,
            _retry_on_exceptions=[InternalServerError]
        )
        assert result == 1337
        assert mock.times_called == 3
        assert mock.times_retried == 2
        


