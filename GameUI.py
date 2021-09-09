# Copyright (c) 2021 Lightricks. All rights reserved.
import re
from abc import ABC, abstractmethod


class GAME_UI(ABC):
    DISPLAY_DICT = {'guess_success': 0, 'guess_failure': 1, 'hint': 2, 'solution': 3}

    @abstractmethod
    def initialize_UI(self):
        pass

    @abstractmethod
    def get_instructions(self):
        pass

    @abstractmethod
    def display_response(self, response):
        pass

    @abstractmethod
    def end_UI(self):
        pass


# Inheritances of UI
class TerminalUI(GAME_UI):
    INSTRUCTIONS = "For guessing a letter enter one, for a hint enter H, for the solution enter S" \
                   "\n "
    WELCOME_MESSAGE = "Hello and Welcome to the best hangman game ever. \n"
    VALID_PATTERN = "[a-z]{1}|H|S"
    BYE_MESSAGE = "Game Over "

    HANGEDMAN = ["00000000000000000000",
                 " 0           0 ",
                 " 0           1",
                 " 0          1  1",
                 " 0            1 ",
                 " 0          3 2 4",
                 " 0         3  2  4",
                 " 0        3   2   4",
                 " 0          5  6",
                 " 0         5     6",
                 " 0        5        6",
                 " 0       5          6",
                 " 0             ",
                 " 0             ",
                 " 0             ",
                 " 0             "]

    def __init__(self):
        self.stages_display = create_stages()
        self.current_display = self.stages_display.pop(0)

    def initialize_UI(self):
        print(TerminalUI.WELCOME_MESSAGE)

    def get_instructions(self):
        user_input = input(TerminalUI.INSTRUCTIONS)
        while not re.match(TerminalUI.VALID_PATTERN, user_input):
            user_input = input("That was invalid input, try again \n" + TerminalUI.INSTRUCTIONS)
        return user_input

    def display_response(self, response):
        response_mode = response[0]
        if response[-1]:
            unique_message = "You already guessed this letter. \n" \
                             " There are {} more guesses left".format(response[2])
        elif response_mode == TerminalUI.DISPLAY_DICT['guess_success']:
            unique_message = "GOOD JOB!! \n" \
                             " Current word" + str(response[1]) \
                             + " There are {} more guesses left".format(response[2])
        elif response_mode == TerminalUI.DISPLAY_DICT['guess_failure']:
            self.current_display = self.stages_display.pop(0)
            if not self.current_display:
                self.current_display = TerminalUI.HANGEDMAN
            unique_message = "WRONG !! \n Current word" + str(response[1]) + \
                             " There are {} more guesses left".format(response[2])
        elif response_mode == TerminalUI.DISPLAY_DICT['hint']:
            unique_message = "The hint is :", response[1]
        else:
            unique_message = "The solution ", response[1]

        for line in self.current_display:
            print(line)
        print(unique_message)

    def end_UI(self):
        print(TerminalUI.BYE_MESSAGE)
        return


def create_stages():
    stages = [TerminalUI.HANGEDMAN.copy()]
    i = 7
    while i > 0:
        current = stages[-1]
        for index, line in enumerate(current):
            current[index] = line.replace(str(i), " ")
        stages.append(current.copy())
        i -= 1

    return stages[::-1]
