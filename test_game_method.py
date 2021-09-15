from GameMethod import HTTPSMethod, HTTPConnection
from unittest.mock import Mock

def test_init_game():
    https_connection = HTTPConnection("a_path")
    https_connection.call_init = \
        Mock(return_value={"hangman": "", "token": "a_token"})
    method = HTTPSMethod(https_connection)
    result = method.initialize_method()
    assert result == ""

