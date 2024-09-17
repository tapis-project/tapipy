from typing import List, Union
from typing_extensions import Literal

from tapipy import errors


class Config:
    def __init__(
        self,
        retries:int = 0,
        retry_delay_sec:int = 0,
        retry_on_exceptions: List[Exception] = [errors.InternalServerError],
        retry_backoff_algo: str = "constant",
        retry_backoff_exponent: int = 2
    ):
        # Validate retries
        if type(retries) != int or retries < 0:
            raise ValueError("Configuration Error: 'retries' must be an integer >= 0")
        
        # Set the number of permitted retries
        self.retries = retries

        # Validate retry_delay_sec
        if type(retry_delay_sec) not in [int, float]:
            raise TypeError("Configuration Error: 'retry_delay_sec' must be an integer or a float")
        
        if retry_delay_sec < 0:
            raise ValueError("Configuration Error: 'retry_delay_sec' must be >= 0")
        
        # Set the retry delay (in seconds)
        self.retry_delay_sec = retry_delay_sec

        # Validate retry_on_exception. Must be a list of exception
        if type(retry_on_exceptions) != list:
            raise TypeError("Configuration Error: 'retry_on_execptions' must be a list of 'Execption' object")
        
        self.retry_on_exceptions = []
        i = 0
        # Validate the type of each item and append to the list of exceptions
        for e in retry_on_exceptions:
            if not issubclass(e, Exception):
                raise TypeError(f"Configuration Error: 'retry_on_execptions' must be a list of class that inherit from 'Execption'. Item at index {i} is of type '{type(e)}'")
            self.retry_on_exceptions.append(e)
            i += 1

        # Validate the backoff algorithm. Must be in the list of valid values
        backoff_algos = ["constant", "exponential"]
        if retry_backoff_algo not in backoff_algos:
            raise ValueError(f"Configuration Error: 'retry_backoff_algo' must be one of the following values: {backoff_algos}")
        
        # Set the backoff algorithm to use for failed retries
        self.retry_backoff_algo = retry_backoff_algo

        # Validate retry_backoff_exponent
        if type(retry_backoff_exponent) != int:
            raise ValueError("Configuration Error: 'retry_backoff_exponent' must be an integer")
        
        self.retry_backoff_exponent = retry_backoff_exponent