from GameMethod import HTTPSMethod, HTTPConnection
from GameState import GameState
from unittest.mock import Mock

def test_init_game():
    https_connection = HTTPConnection("a_path")
    https_connection.init_game = Mock(
        return_value={"hangman": "", "token": "a_token"}
    )
    method = HTTPSMethod(https_connection)

    result = method.initialize_method()

    assert result == ""

def test_correct_guess():
    expected = GameState(
        GameState.MODE_DICT['guess_success'],
        "",
        6,
        False
    )
    https_connection = HTTPConnection("a_path")
    https_connection.send_guess = Mock(
        return_value={"hangman": "", "":""}
    )
    method = HTTPSMethod(https_connection)
    user_input = "u"

    result = method.play_one_turn(user_input)

    assert result == {}

