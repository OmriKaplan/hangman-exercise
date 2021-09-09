# Copyright (c) 2021 Lightricks. All rights reserved.


class Game:

    def __init__(self, user_interface, game_method):
        self.user_interface = user_interface
        self.game_method = game_method
        self.hangman_string = self.game_method.initialize_method()

    def operate_game(self):
        self.user_interface.initialize_UI()
        while not self.game_method.is_game_finished():
            user_input = self.user_interface.get_instructions()
            response = self.game_method.play_one_turn(user_input)
            self.user_interface.display_response(response)
        self.user_interface.end_UI()
