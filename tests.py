# Copyright (c) 2021 Lightricks. All rights reserved.
import json
import subprocess
import unittest
from Game import Game
from GameMethod import DummyMethod, HTTPSMethod, EmptyMethod, GameMethod
from GameUI import TerminalUI, TestUI
import requests
import pytest

# CONSTANTS
INSTRUCTIONS = "For guessing a letter enter one, for a hint enter H, for the solution enter S" \
               "\n "
WELCOME_MESSAGE = "Hello and Welcome to the best hangman game ever. \n"
VALID_PATTERN = "[a-z]{1}|H|S"
BYE_MESSAGE = "Game Over "
UI_OUTPUTS = [WELCOME_MESSAGE, INSTRUCTIONS, VALID_PATTERN, BYE_MESSAGE]

EMPTY_SUCCESS = "Hello and Welcome to the best hangman game ever. \n\nGame Over \n"


# FUNCTIONS
def validate_JSON(json_data):
    """
    This function validates json format on a given data structure
    :param json_data:
    :return: True if it is, False otherwise
    """
    try:
        json.loads(json_data)
    except ValueError as err:
        return False
    return True


def edit_distance(string1, string2):
    """
    This function checks the length of the edit distance between two given strings
    or in other words - how many operations should i do in order to get from string1 to string2.
    Assumptions: The strings in this project are necessarily in the same length.
    :param string1:
    :param string2:
    :return: the distance
    """
    count_diffs = 0
    for a, b in zip(string1, string2):
        if a != b:
            count_diffs += 1
    return count_diffs


# CLASSES

class TestClassCheckAPI(unittest.TestCase):
    """
    This test class was created in order to check the API that was given in this exercise.
    """

    def setUp(self):
        """
        the testing framework executes the test setup method first,
        before any test method in the class. It includes all the required data for each test.
        """
        self.url = "https://hangman-api.herokuapp.com/hangman"
        self.response = requests.post(self.url, data='text=great').json()
        self.game_token = self.response['token']
        self.hangman_string = self.response['hangman']

    def test_types(self):
        """
        Checks if the API sends valid & expected types: JSON, DICT etc.
        :return:
        """
        response = requests.post(self.url, data='text=great')
        assert str(type(response)) == "<class 'requests.models.Response'>"
        response = response.json()
        assert str(type(response)) == "<class 'dict'>"

    def test_valid_login(self):
        response = requests.post(self.url, data='text=great')
        assert response.status_code == 200
        keys = set(response.json().keys())
        assert keys == {'hangman', 'token'}

    def test_valid_get_hint(self):
        response = requests.get(self.url + '/hint', data={'token': self.game_token})
        assert response.status_code == 200
        keys = set(response.json().keys())
        assert keys == {'hint', 'token'}

    def test_valid_guess(self):
        response = requests.put(self.url, data={'token': self.game_token, 'letter': 'k'})
        assert response.status_code == 200
        keys = set(response.json().keys())
        assert keys == {'hangman', 'token', 'correct'}

    def test_repeating_guess(self):
        response = requests.put(self.url, data={'token': self.game_token, 'letter': 'l'})
        game_token = response.json()['token']
        response = requests.put(self.url, data={'token': game_token, 'letter': 'l'})
        assert response.status_code == 304

    @pytest.mark.skip
    def test_invalid_guess(self):
        response = requests.put(self.url, data={'token': self.game_token, 'letter': 'dl'})
        assert response.status_code != 200

    def test_valid_get_solution(self):
        response = requests.get(self.url, data={'token': self.game_token})
        assert response.status_code == 200
        keys = set(response.json().keys())
        assert keys == {'solution', 'token'}

    def tearDown(self):
        self.test_data = []


class TestClassGame(unittest.TestCase):

    def setUp(self):
        """
       the testing framework executes the test setup method first,
       before any test method in the class. It includes all the required data for each test.
        """
        # Creation of UIs
        self.test_ui = TestUI()
        self.test_terminal_ui = TerminalUI()

        # Creation of Methods
        self.test_empty = EmptyMethod()
        self.test_dummy_method = DummyMethod()
        self.test_https = HTTPSMethod()

        # Creation of Games
        self.test_game_empty = Game(self.test_terminal_ui, self.test_empty)
        self.test_game_https = Game(self.test_terminal_ui, self.test_https)
        self.test_games = [self.test_game_https, self.test_game_empty]

    @pytest.mark.skip
    def test_integration(self):
        """ Checks if an empty victory works as expected """
        for test_index, test_game in enumerate(self.test_games[1:]):
            proc = subprocess.Popen(['python', '/Users/kbenarie/Projects/hangman-exercise/main.py'],
                                    stdout=subprocess.PIPE)
            stdout = proc.stdout.read().decode('utf-8')
            assert stdout == EMPTY_SUCCESS, 'empty case did not succeed'

    # Game Method Tests

    def test_hangman_string_changes_when_needed_game_method(self):
        letters = ['a', 5, 'b', 'd', 'ff', '']

        for user_input in letters:
            hangman_string_before_guess = self.test_https.initialize_method()
            hangman_string_after_guess = self.test_https.play_one_turn(user_input).output
            # checks if the edit distance is less or equal to 1
            assert edit_distance(hangman_string_before_guess, hangman_string_after_guess) in {0, 1}

    def test_guesses_number_goes_down_game_method(self):
        letters = ['a', 5, 'b', 'd', 'ff', '']
        guesses_number_before = self.test_https.play_one_turn(letters[0]).guesses_left

        for user_input in letters[1:]:
            guesses_number_after = self.test_https.play_one_turn(user_input).guesses_left
            # checks if the guesses number allowed goes down
            assert guesses_number_before >= guesses_number_after

    def test_invalid_guess_game_method(self):
        letters = ['4', 5, '', 'ff', '%']
        response = self.test_https.play_one_turn(letters[0])
        guesses_number_before, hangman_string_before_guess = response.guesses_left, response.output
        for user_input in letters[1:]:
            response = self.test_https.play_one_turn(user_input)
            guesses_number_after, hangman_string_after_guess = response.guesses_left, response.output
            assert guesses_number_after == guesses_number_before
            assert hangman_string_after_guess == hangman_string_before_guess
            assert response.current_mode == -1

    def test_repeating_guess_game_method(self):
        # repeating char - a
        response = self.test_https.play_one_turn('a')
        guesses_number_before, hangman_string_before_guess = response.guesses_left, response.output
        response = self.test_https.play_one_turn('a')
        guesses_number_after, hangman_string_after_guess = response.guesses_left, response.output
        assert guesses_number_after == guesses_number_before
        assert hangman_string_after_guess == hangman_string_before_guess

    # UI Tests

    def test_initiate_ui(self):
        assert self.test_ui.initialize_UI() == WELCOME_MESSAGE

    def test_end_ui(self):
        assert self.test_ui.end_UI() == BYE_MESSAGE

    def test_instructions_ui(self):
        assert self.test_ui.get_instructions() == INSTRUCTIONS

    def test_invalid_guess_ui(self):
        response = self.test_https.play_one_turn('5')
        current_state = self.test_ui.display_response(response)
        assert current_state.current_mode == -1

    def test_repeating_guess_ui(self):
        response1 = self.test_https.play_one_turn('a')
        current_state1 = self.test_ui.display_response(response1)
        response2 = self.test_https.play_one_turn('a')
        current_state2 = self.test_ui.display_response(response2)
        assert current_state2.already_guessed
        assert current_state2.current_mode == 1
        assert current_state1.output == current_state2.output

    def test_successful_guess_ui(self):
        hangman = '__r_n'
        response = self.test_dummy_method.play_one_turn('k')
        current_state = self.test_ui.display_response(response)
        assert current_state.current_mode == 0
        assert edit_distance(current_state.output, hangman) == 1
        hangman_after_k = current_state.output

        response = self.test_dummy_method.play_one_turn('e')
        current_state = self.test_ui.display_response(response)
        assert current_state.current_mode == 0
        assert edit_distance(current_state.output, hangman_after_k) == 2

    def test_unsuccessful_guess_ui(self):
        hangman = '__r_n'
        response = self.test_dummy_method.play_one_turn('b')
        current_state = self.test_ui.display_response(response)
        assert current_state.current_mode == 1
        assert edit_distance(current_state.output, hangman) == 0

    def test_hint_request_ui(self):
        response = self.test_dummy_method.play_one_turn('H')
        current_state = self.test_ui.display_response(response)
        assert current_state.current_mode == 2
        is_hint_valid = bool(GameMethod.GUESS_REGEX.fullmatch(response.output))
        assert is_hint_valid

    def test_solution_ui(self):
        response = self.test_dummy_method.play_one_turn('S')
        current_state = self.test_ui.display_response(response)
        assert current_state.current_mode == 3
        assert current_state.output == 'keren'
