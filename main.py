# Copyright (c) 2021 Lightricks. All rights reserved.
from Game import Game
from GameMethod import DummyMethod, HTTPSMethod, EmptyMethod
from GameUI import TerminalUI


def main():
    ui = TerminalUI()
    #method = HTTPSMethod()
    method = EmptyMethod()
    game = Game(ui, method)
    game.operate_game()


if __name__ == "__main__":
    main()
