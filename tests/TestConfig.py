import unittest

from tapipy.configuration import Config


class TestConfig(unittest.TestCase):
    def testNoErrors(self):
        try:
            Config()
            Config(
                retries=5,
                retry_on_exceptions=[ValueError],
                retry_backoff_algo="exponential",
                retry_backoff_exponent=2,
                retry_delay_sec=5
            )
        except Exception as e:
            self.fail(str(e))
        

    def testMisconfigured(self):
        self.assertRaises(ValueError, Config, retries=1.5) # Only integers
        self.assertRaises(ValueError, Config, retries=-1) # Must be >= 0
        self.assertRaises(TypeError, Config, retry_on_exceptions={}) # Must be list
        self.assertRaises(TypeError, Config, retry_on_exceptions=["NotException"]) # Items must be a subclass of Exception
        self.assertRaises(TypeError, Config, retry_delay_sec="notNumber") # Must be number
        self.assertRaises(ValueError, Config, retry_delay_sec=-1) # Must >= 0

        # retry_backoff_algo: str = "constant",
        # retry_backoff_exponent: int = 2