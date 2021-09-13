# Copyright (c) 2021 Lightricks. All rights reserved.

class GameState:

    MODE_DICT = {
        'guess_success': 0, 'guess_failure': 1, 'hint': 2,
        'solution': 3, 'invalid': -1
    }

    def __init__(self, current_mode, output, guesses_left, already_guessed):
        self.current_mode = current_mode
        self.output = output
        self.guesses_left = guesses_left
        self.already_guessed = already_guessed
