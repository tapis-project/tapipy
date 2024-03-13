import unittest

from functools import partial

from tapipy.util import constant_time, exponential_time, backoff
from tapipy.errors import TapyClientConfigurationError


class TestUtils(unittest.TestCase):
    def testConstantTime(self):
        assert constant_time(0) == 0
        assert constant_time(1) == 1

    def testExponentialTime(self):
        assert exponential_time(0) == 0
        assert exponential_time(1) == 2
        assert exponential_time(2) == 4
        assert exponential_time(2, _retry_exponent=3) == 8

    def testBackoff(self):
        assert backoff(0, algo="constant") == 0
        assert backoff(0, algo="exponential") == 0
        self.assertRaises(
            TapyClientConfigurationError,
            partial(backoff, 0, algo="INVALID_ALGO")
        )
        