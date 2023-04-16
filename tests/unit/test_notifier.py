import pytest, json, sys
sys.path.append('app')
import notifier.notifier as notifier 

def test_notifier():
    '''Formats the directory and verifies that all files ended up where they should be'''
    message = notifier.send_error_notification("Test Subject from DTS", "Test Body from DTS", "dts@hu.onmicrosoft.com")
    json_message = json.loads(message)
    assert type(json_message) is dict
