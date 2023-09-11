import pytest
import sys
from celery.result import AsyncResult
sys.path.append('app')
import notifier.notifier as notifier 

def test_notifier():
    '''Formats the directory and verifies that all files ended up where they should be'''
    result = notifier.send_error_notification("Test Subject from DTS", "Test Body from DTS", "dts@hu.onmicrosoft.com")
    assert isinstance(result, AsyncResult)
