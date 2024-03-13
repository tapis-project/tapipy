import unittest

from .mocks import RetriableMock
from tapipy.errors import InternalServerError


class TestRetriableDecorator(unittest.TestCase):
    def testRetriableCallsOnce(self):
        # NOTE Retriable decorator can be found on the __call__ method of the
        # RetriableMock
        mock = RetriableMock()
        mock()
        assert mock.times_called == 1
        assert mock.times_retried == 0

    def testRetriableMisconfigured(self):
        mock = RetriableMock(result=1337)
        assert mock(_retries=0) == 1337
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

    def testRetriableRaisesExceptionDifferentThanSpecifiedRetryOn(self):
        mock = RetriableMock(
            raises=TypeError,
            succeeds_on_nth_retry=None # Fails forever
        )

        self.assertRaises(
            TypeError,
            mock,
            _retries=3,
            _retry_on_exceptions=[ValueError]
        )
        assert mock.times_called == 1
        assert mock.times_retried == 0
        
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

    def testRetriableSucceedsOnFirstRetry(self):
        mock = RetriableMock(
            raises=InternalServerError,
            succeeds_on_nth_retry=1,
            result=1337
        )
        result = mock(
            _retries=1,
            _retry_on_exceptions=[InternalServerError]
        )
        assert result == 1337
        assert mock.times_called == 2
        assert mock.times_retried == 1
        
    def testRetriableFirstArgIsSelfPlusArgsKwargsZeroRetries(self):
        mock = RetriableMock(result=1337)
        args = ("arg1", "arg2")
        kwargs = {"kwarg1":1, "kwarg2":2}
        result = mock(*args, **kwargs)
        assert result == 1337
        assert mock.times_called == 1
        assert mock.times_retried == 0

        # Testing args kwargs
        assert isinstance(mock.args[0], RetriableMock) # Self is first arg
        assert "arg1" in mock.args and mock.args[1] == "arg1"
        assert "arg2" in mock.args and mock.args[2] == "arg2"
        assert "kwarg1" in mock.kwargs and mock.kwargs.get("kwarg1") == 1
        assert "kwarg2" in mock.kwargs and mock.kwargs.get("kwarg2") == 2

    def testRetriableFirstArgIsSelfPlusArgsKwargsAndNRetries(self):
        mock = RetriableMock(
            raises=InternalServerError,
            succeeds_on_nth_retry=2,
            result=1337
        )
        args = ("arg1", "arg2")
        kwargs = {"kwarg1":1, "kwarg2":2}
        result = mock(
            *args,
            _retries=2,
            **kwargs
        )
        assert result == 1337
        assert mock.times_called == 3
        assert mock.times_retried == 2

        # Testing args kwargs
        assert isinstance(mock.args[0], RetriableMock)
        assert "arg1" in mock.args and mock.args[1] == "arg1"
        assert "arg2" in mock.args and mock.args[2] == "arg2"
        assert "kwarg1" in mock.kwargs and mock.kwargs.get("kwarg1") == 1
        assert "kwarg2" in mock.kwargs and mock.kwargs.get("kwarg2") == 2


