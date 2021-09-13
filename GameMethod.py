# Copyright (c) 2021 Lightricks. All rights reserved.
from abc import ABC, abstractmethod
import requests
# An abstract class - Server
import re

from Game import Game
from GameState import GameState


class GameMethod(ABC):
    GUESS_PATTERN = "[a-z]{1}"
    GUESS_REGEX = re.compile(GUESS_PATTERN)
    HINT_PATTERN = "[H]{1}"
    HINT_REGEX = re.compile(HINT_PATTERN)
    SOLUTION_PATTERN = "[S]{1}"
    SOLUTION_REGEX = re.compile(SOLUTION_PATTERN)
    EMPTY_CELL = '_'
    RESPONSE_DICT = {
        'guess_success': 0, 'guess_failure': 1, 'hint': 2,
        'solution': 3, 'invalid': -1
    }

    @abstractmethod
    def initialize_method(self):
        pass

    @abstractmethod
    def play_one_turn(self, user_input):
        pass

    @abstractmethod
    def is_game_finished(self):
        pass


# Inheritances of Server
class HTTPSMethod(GameMethod):
    PATH = "https://hangman-api.herokuapp.com/hangman"
    HINT_PATH = PATH + "/hint"

    def __init__(self):
        self.start = requests.post(HTTPSMethod.PATH).json()
        self.hangman_string, self.game_token = self.start['hangman'], self.start['token']
        self.guesses_left = 6
        self.asked_for_solution = False

    def initialize_method(self):
        return self.hangman_string

    def is_game_finished(self):
        if self.asked_for_solution:
            return True
        return GameMethod.EMPTY_CELL not in self.hangman_string

    def play_one_turn(self, user_input):
        already_guessed, correct = False, False
        user_input = str(user_input)
        guess_match = bool(GameMethod.GUESS_REGEX.fullmatch(user_input))
        hint_match = bool(GameMethod.HINT_REGEX.fullmatch(user_input))
        sol_match = bool(GameMethod.SOLUTION_REGEX.fullmatch(user_input))
        if guess_match:  # guess mode
            requests_answer = requests.put(HTTPSMethod.PATH, data={
                'token': self.game_token,
                'letter': user_input})
            if 304 == requests_answer.status_code:
                already_guessed = True
            else:
                requests_answer = requests_answer.json()
                self.hangman_string, self.game_token, correct = requests_answer['hangman'], \
                                                                requests_answer['token'], \
                                                                requests_answer['correct']
                self.guesses_left -= 1
            current_state = GameState(int(not correct), self.hangman_string, self.guesses_left, already_guessed)
            return current_state
        elif hint_match:
            requests_answer = requests.get(HTTPSMethod.HINT_PATH,
                                           data={'token': self.game_token}).json()
            self.game_token, hint = requests_answer['token'], requests_answer['hint']
            current_state = GameState(GameMethod.RESPONSE_DICT['hint'], hint, self.guesses_left, already_guessed)
            return current_state
        elif sol_match:
            self.asked_for_solution = True
            requests_answer = requests.get(HTTPSMethod.PATH,
                                           data={'token': self.game_token}).json()
            self.game_token, game_solution = requests_answer['token'], requests_answer['solution']
            current_state = GameState(GameMethod.RESPONSE_DICT['solution'], game_solution,
                   self.guesses_left, already_guessed)
            return current_state
        else:
            current_state = GameState(GameMethod.RESPONSE_DICT['invalid'], self.hangman_string, self.guesses_left, already_guessed)
            return current_state


def update_string(hangman_string, solution, user_input):
    new_hangman_string = ''
    for hang, sol in zip(hangman_string, solution):
        if hang == '_' and sol == user_input:
            new_hangman_string += user_input
        else:
            new_hangman_string += hang
    return new_hangman_string


class DummyMethod(GameMethod):

    def __init__(self):
        self.hangman_string = '__r_n'
        self.guesses = []
        self.solution = "keren"
        self.guesses_allowed = 6
        self.asked_for_solution = False

    def initialize_method(self):
        return self.hangman_string

    def is_game_finished(self):
        if self.asked_for_solution:
            return True
        return GameMethod.EMPTY_CELL not in self.hangman_string

    def play_one_turn(self, user_input):
        guess_match = bool(GameMethod.GUESS_REGEX.fullmatch(user_input))
        hint_match = bool(GameMethod.HINT_REGEX.fullmatch(user_input))
        sol_match = bool(GameMethod.SOLUTION_REGEX.fullmatch(user_input))
        if guess_match:  # guess mode
            if user_input not in self.guesses:
                self.guesses.append(user_input)
            if user_input in self.solution:
                self.hangman_string = update_string(self.hangman_string, self.solution, user_input)
                current_state = GameState(GameMethod.RESPONSE_DICT['guess_success'], self.hangman_string, \
                       self.guesses_allowed - len(self.guesses), False)
                return current_state
            else:
                current_state = GameState(GameMethod.RESPONSE_DICT['guess_failure'], self.hangman_string, \
                       self.guesses_allowed - len(self.guesses), False)
                return current_state
        elif hint_match:
            current_state = GameState(GameMethod.RESPONSE_DICT['hint'], 'c', self.guesses_allowed - len(self.guesses), False)
            return current_state
        elif sol_match:
            self.asked_for_solution = True
            current_state = GameState(GameMethod.RESPONSE_DICT['solution'], self.solution, len(self.guesses), False)
            return current_state


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
