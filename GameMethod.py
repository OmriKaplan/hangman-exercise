# Copyright (c) 2021 Lightricks. All rights reserved.
from abc import ABC, abstractmethod
import requests
# An abstract class - Server
import re

from Game import Game


class GameMethod(ABC):
    GUESS_PATTERN = "[a-z]{1}"
    HINT_PATTERN = "H"
    SOLUTION_PATTERN = "S"
    EMPTY_CELL = '_'
    RESPONSE_DICT = {
        'guess_success': 0, 'guess_failure': 1, 'hint': 2,
        'solution': 3
    }

    @abstractmethod
    def initialize_method(self):
        pass

    @abstractmethod
    def play_one_turn(self, user_input):
        pass


# Inheritances of Server
class HTTPSMethod(GameMethod):
    PATH = "https://hangman-api.herokuapp.com/hangman"

    def __init__(self):
        self.start = requests.post \
            (HTTPSMethod.PATH, data='text=great').json()
        self.hangman_string, self.game_token = self.start['hangman'], self.start[
            'token']
        self.guesses_left = 6
        self.asked_for_solution = False

    def initialize_method(self):
        return self.hangman_string

    def is_game_finished(self):
        if self.asked_for_solution:
            return True
        return GameMethod.EMPTY_CELL not in self.hangman_string

    def play_one_turn(self, user_input):
        already_guessed = False
        guess_match = re.match(GameMethod.GUESS_PATTERN, user_input)
        hint_match = re.match(GameMethod.HINT_PATTERN, user_input)
        sol_match = re.match(GameMethod.SOLUTION_PATTERN, user_input)
        if guess_match:  # guess mode
            requests_answer = requests.put(self.game_token, user_input)
            if '304' in requests_answer:
                already_guessed = True
            else:
                self.hangman_string, self.game_token, correct = requests_answer
                self.guesses_left -= 1
            return int(not correct), self.hangman_string, self.guesses_left, already_guessed
        elif hint_match:
            hint, self.game_token = requests.get("https://hangman-api.herokuapp.com/hangman/hint",
                                                 self.game_token)
            return GameMethod.RESPONSE_DICT['hint'], hint, self.guesses_left, already_guessed
        elif sol_match:
            self.asked_for_solution = True
            game_solution, self.game_token = requests.get(HTTPSMethod.PATH, self.game_token)
            return GameMethod.RESPONSE_DICT['solution'], game_solution, \
                   self.guesses_left, already_guessed


class DummyMethod(GameMethod):

    def __init__(self):
        self.hangman_string = 'fdgfdgd____'
        self.guesses = []
        self.solution = "sfdjkshdfjsd"
        self.guesses_allowed = 6
        self.asked_for_solution = False

    def initialize_method(self):
        return self.hangman_string

    def is_game_finished(self):
        if self.asked_for_solution:
            return True
        return GameMethod.EMPTY_CELL not in self.hangman_string

    def play_one_turn(self, user_input):
        guess_match = re.match(GameMethod.GUESS_PATTERN, user_input)
        hint_match = re.match(GameMethod.HINT_PATTERN, user_input)
        sol_match = re.match(GameMethod.SOLUTION_PATTERN, user_input)
        if guess_match:  # guess mode
            if user_input not in self.guesses:
                self.guesses.append(user_input)
            if user_input in self.solution:
                self.hangman_string = 'sfkjsds__'
                return GameMethod.RESPONSE_DICT['guess_success'], self.hangman_string, \
                       self.guesses_allowed - len(self.guesses), False
            else:
                return GameMethod.RESPONSE_DICT['guess_failure'], self.hangman_string, \
                       self.guesses_allowed - len(self.guesses), False
        elif hint_match:
            return GameMethod.RESPONSE_DICT['hint'], 'c', self.guesses_allowed - len(self.guesses)
        elif sol_match:
            self.asked_for_solution = True
            return GameMethod.RESPONSE_DICT['solution'], self.solution, len(self.guesses), False


class EmptyMethod(GameMethod):
    def __init__(self):
        self.hangman_string = ''
        self.guesses = []
        self.solution = ''
        self.guesses_allowed = 6
        self.asked_for_solution = False

    def initialize_method(self):
        return self.hangman_string

    def is_game_finished(self):
        if self.asked_for_solution:
            return True
        return GameMethod.EMPTY_CELL not in self.hangman_string

    def play_one_turn(self, user_input):
        guess_match = re.match(GameMethod.GUESS_PATTERN, user_input)
        hint_match = re.match(GameMethod.HINT_PATTERN, user_input)
        sol_match = re.match(GameMethod.SOLUTION_PATTERN, user_input)
        pass
