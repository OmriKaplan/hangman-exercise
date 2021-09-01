# Copyright (c) 2021 Lightricks. All rights reserved.
import re

from Server import DummyServer
from UI import TerminalUI


class Game:
    INSTRUCTIONS = "For guessing a letter enter one, for a hint enter H, for the solution enter S " \
                   "\n "
    WELCOME_MESSAGE = "Hello and Welcome to the best hangman game ever. \n"
    GUESS_PATTERN = "[a-z]{1}"
    HINT_PATTERN = "H"
    SOL_PATTERN = "S"
    INPUT_DICT = {"letter": 1, "hint": 2, "sol": 3, "invalid": -1}
    GET_DICT = {"hint": 0, "sol": 1}
    EMPTY_CELL = '_'
    END_MESSAGE = 'BYE !'

    def __init__(self):
        self.lives = 6
        self.user_interface = TerminalUI()  #TODO change
        self.api = DummyServer()
        self.game_token, self.hangman_string = self.api.initialize_server()

    def is_game_finished(self):
        return 'EMPTY_CELL' in self.hangman_string

    def end_game(self):
        self.user_interface.end_UI()

    def guess_letter(self, letter):
        self.word, self.game_token, correct = self.api.send_to_server(self.game_token, letter)
        return correct, None

    def get_hint(self):
        hint, self.game_token = self.api.get_from_server(req_type=Game.GET_DICT['hint'])
        return True, "Your hint is: " + hint

    def parse_input(self, user_input):
        guess_match = re.match(Game.GUESS_PATTERN, user_input)
        if guess_match:
            return Game.INPUT_DICT['letter']
        hint_match = re.match(Game.HINT_PATTERN, user_input)
        if hint_match:
            return Game.INPUT_DICT['hint']
        sol_match = re.match(Game.SOL_PATTERN, user_input)
        if sol_match:
            return Game.INPUT_DICT['sol']
        return Game.INPUT_DICT['invalid']

    def get_solution(self):
        sol, self.game_token = self.api.get_from_server(req_type=Game.GET_DICT['sol'])
        return True, "The solution is: " + sol

    def send_error_message(self):
        return 'input is invalid'

    def single_turn(self):
        user_input = input(Game.INSTRUCTIONS)  # TODO UI's JOB
        input_state = self.parse_input(user_input)
        func_dict = {
            Game.INPUT_DICT['letter']: self.guess_letter(user_input),
            Game.INPUT_DICT['hint']: self.get_hint(),
            Game.INPUT_DICT['sol']: self.get_solution(),
            Game.INPUT_DICT['invalid']: self.send_error_message(),
        }
        response = func_dict[input_state]
        self.user_interface.update_UI_then_display(move_stage_forward=not response[0],
                                                   show=response[1],
                                                   current=self.hangman_string)

    def operate_game(self):
        self.user_interface.initialize_UI(Game.WELCOME_MESSAGE)
        while not self.is_game_finished():
            self.single_turn()
        self.end_game()
