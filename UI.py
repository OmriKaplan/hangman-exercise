# Copyright (c) 2021 Lightricks. All rights reserved.
from abc import ABC, abstractmethod


class UI(ABC):
    @abstractmethod
    def initialize_UI(self, welcome_message):
        pass

    @abstractmethod
    def update_UI_then_display(self, move_stage_forward, show, current):
        pass

    @abstractmethod
    def _display_UI(self, show, current, guesses_num):
        pass

    @abstractmethod
    def end_UI(self, bye_message):
        pass


# Inheritances of UI
class TerminalUI(UI):

    def __init__(self):
        self.current_stage = TerminalUI.STAGE_ZERO

    STAGE_ZERO = \
        ["00000000000000000000",
         " 0           0 ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             "]

    STAGE_ONE = \
        ["00000000000000000000",
         " 0           0 ",
         " 0           1",
         " 0          1  1",
         " 0            1  ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             "]

    STAGE_TWO = \
        ["00000000000000000000",
         " 0           0 ",
         " 0           1",
         " 0          1  1",
         " 0            1 ",
         " 0            2 ",
         " 0            2",
         " 0            2",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             "]

    STAGE_THREE = \
        ["00000000000000000000",
         " 0           0 ",
         " 0           1",
         " 0          1  1",
         " 0            1 ",
         " 0          3 2 ",
         " 0         3  2",
         " 0        3   2",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             "]

    STAGE_FOUR = \
        ["00000000000000000000",
         " 0           0 ",
         " 0           1",
         " 0          1  1",
         " 0            1 ",
         " 0          3 2 4",
         " 0         3  2  4",
         " 0        3   2   4",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             "]

    STAGE_FIVE = \
        ["00000000000000000000",
         " 0           0 ",
         " 0           1",
         " 0          1  1",
         " 0            1 ",
         " 0          3 2 4",
         " 0         3  2  4",
         " 0        3   2   4",
         " 0          5  ",
         " 0         5    ",
         " 0        5        ",
         " 0       5          ",
         " 0             ",
         " 0             ",
         " 0             ",
         " 0             "]

    STAGE_SIX = \
        ["00000000000000000000",
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

    STAGES = [STAGE_ZERO, STAGE_ONE, STAGE_TWO, STAGE_THREE, STAGE_FOUR, STAGE_FIVE, STAGE_SIX]
    CURRENT_STAGE_INDEX = 0

    def initialize_UI(self, welcome_message):
        print(welcome_message)

    def update_UI_then_display(self, move_stage_forward, show, current):
        if move_stage_forward:
            TerminalUI.CURRENT_STAGE_INDEX += 1
            self.current_stage = TerminalUI.STAGES[TerminalUI.CURRENT_STAGE_INDEX]
        self._display_UI(show, current, len(TerminalUI.STAGES) - 1 - TerminalUI.CURRENT_STAGE_INDEX)
        # doesn't make sense to put the guesses here, think about another idea !!!!!!

    def _display_UI(self, show, current, guesses_num):
        # doesn't make sense to put the guesses here, think about another idea !!!!
        for line in self.current_stage:
            print(line)
        if show:
            print(show)
        print(current, "-", str(guesses_num) + " Guesses remaining")

    def end_UI(self, bye_message):
        print(bye_message)
        return
