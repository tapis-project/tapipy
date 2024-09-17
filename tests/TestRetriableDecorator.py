import unittest

from .mocks import OperationMock
from tapipy.errors import InternalServerError
from tapipy.configuration import Config


class TestRetriableDecorator(unittest.TestCase):
    def testRetriableCallsOnce(self):
        # NOTE Retriable decorator can be found on the __call__ method of the
        # OperationMock
        mock_op = OperationMock()
        mock_op()
        assert mock_op.times_called == 1
        assert mock_op.times_retried == 0
    
    def testRetriableRaisesSpecifedExceptionWhichOverridesDefault(self):
        _ = OperationMock(
            raises=InternalServerError,
            succeeds_on_nth_retry=None, # Fails forever
            config=Config(retries=3, retry_on_exceptions=[TypeError])
        )
        mock2 = OperationMock(
            raises=TypeError,
            succeeds_on_nth_retry=None # Fails forever
        )

        self.assertRaises(
            TypeError,
            mock2,
        )

    def testRetriableRaisesExceptionDifferentThanSpecifiedRetryOn(self):
        mock_op = OperationMock(
            raises=TypeError,
            succeeds_on_nth_retry=None, # Fails forever
            config=Config(retries=3, retry_on_exceptions=[ValueError])
        )

        self.assertRaises(
            TypeError,
            mock_op,
        )
        assert mock_op.times_called == 1
        assert mock_op.times_retried == 0
        
    def testRetriableRetriesUntilRetryLimitReached(self):
        mock_op = OperationMock(
            raises=InternalServerError,
            succeeds_on_nth_retry=None, # Fails forever
            config=Config(retries=3, retry_on_exceptions=[InternalServerError])
        )
        self.assertRaises(
            InternalServerError,
            mock_op,
        )
        assert mock_op.times_called == 4
        assert mock_op.times_retried == 3

    def testRetriableSuccedsBeforeReachingRetryLimit(self):
        mock_op = OperationMock(
            raises=InternalServerError,
            succeeds_on_nth_retry=2,
            result=1337,
            config=Config(retries=3, retry_on_exceptions=[InternalServerError])
        )
        result = mock_op()
        assert result == 1337
        assert mock_op.times_called == 3
        assert mock_op.times_retried == 2

    def testRetriableSucceedsOnFirstRetry(self):
        mock_op = OperationMock(
            raises=InternalServerError,
            succeeds_on_nth_retry=1,
            result=1337,
            config=Config(retries=1, retry_on_exceptions=[InternalServerError])
        )
        result = mock_op()
        assert result == 1337
        assert mock_op.times_called == 2
        assert mock_op.times_retried == 1

    def testSucceedsWithClientConfigOverrideViaCallMethod(self):
        mock_op = OperationMock(
            raises=ValueError,
            succeeds_on_nth_retry=1,
            result=1337
        )
        result = mock_op(
            _config=Config(retries=1, retry_on_exceptions=[ValueError])
        )
        assert result == 1337
        assert mock_op.times_called == 2
        assert mock_op.times_retried == 1
        
    def testRetriableFirstArgIsSelfPlusArgsKwargsZeroRetries(self):
        mock_op = OperationMock(result=1337)
        args = ("arg1", "arg2")
        kwargs = {"kwarg1":1, "kwarg2":2}
        result = mock_op(*args, **kwargs)
        assert result == 1337
        assert mock_op.times_called == 1
        assert mock_op.times_retried == 0

        # Testing args kwargs
        assert isinstance(mock_op.args[0], OperationMock) # Self is first arg
        assert "arg1" in mock_op.args and mock_op.args[1] == "arg1"
        assert "arg2" in mock_op.args and mock_op.args[2] == "arg2"
        assert "kwarg1" in mock_op.kwargs and mock_op.kwargs.get("kwarg1") == 1
        assert "kwarg2" in mock_op.kwargs and mock_op.kwargs.get("kwarg2") == 2

    def testRetriableFirstArgIsSelfPlusArgsKwargsAndNRetries(self):
        mock_op = OperationMock(
            raises=InternalServerError,
            succeeds_on_nth_retry=2,
            result=1337,
            config=Config(retries=2),
        )
        args = ("arg1", "arg2")
        kwargs = {"kwarg1":1, "kwarg2":2}
        result = mock_op(
            *args,
            **kwargs
        )
        assert result == 1337
        assert mock_op.times_called == 3
        assert mock_op.times_retried == 2

        # Testing args kwargs
        assert isinstance(mock_op.args[0], OperationMock)
        assert "arg1" in mock_op.args and mock_op.args[1] == "arg1"
        assert "arg2" in mock_op.args and mock_op.args[2] == "arg2"
        assert "kwarg1" in mock_op.kwargs and mock_op.kwargs.get("kwarg1") == 1
        assert "kwarg2" in mock_op.kwargs and mock_op.kwargs.get("kwarg2") == 2


