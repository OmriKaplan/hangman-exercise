# Copyright (c) 2021 Lightricks. All rights reserved.
import os
import subprocess
import sys
import module
import pytest
from py import test

from Game import Game
from GameMethod import DummyMethod, HTTPSMethod, EmptyMethod
from GameUI import TerminalUI


@pytest.fixture
def parameters():
    instructions = "For guessing a letter enter one, for a hint enter H, for the solution enter S" \
                   "\n "
    welcome_message = "Hello and Welcome to the best hangman game ever. \n"
    valid_input_pattern = "[a-z]{1}|H|S"
    end_message = "Game Over "
    test_ui = TerminalUI()
    test_methods = [DummyMethod(), HTTPSMethod()]
    test_games = [Game(test_ui, test_method) for test_method in test_methods]


# @pytest.mark.parametrize("x, y, z", [(3,4,6), (2,4,6)])

DUMMY_INPUTS = {
    'initial_hangman': 'fdgfdgd____', 'solution': "sfdjkshdfjsd", 'guesses_allowed': 6,
    'guesses': ['f', 'd', '3']
}

INSTRUCTIONS = "For guessing a letter enter one, for a hint enter H, for the solution enter S" \
               "\n "
WELCOME_MESSAGE = "Hello and Welcome to the best hangman game ever. \n"
VALID_PATTERN = "[a-z]{1}|H|S"
BYE_MESSAGE = "Game Over "

UI_OUTPUTS = [WELCOME_MESSAGE, INSTRUCTIONS, VALID_PATTERN, BYE_MESSAGE]

# API TESTS
"""
def test_valid_login(url):
    response = requests.post(url, data='text=great').json()
    assert response.status_code == 200

def test_valid_get_hint(url):
    response = requests.get(url, data='text=great').json()
    assert response.status_code == 200

def test_valid_guess(url):
    response = requests.put(url, data='text=great').json()
    assert response.status_code == 200

def test_valid_get_solution(url):
    response = requests.get(url, data='text=great').json()
    assert response.status_code == 200
"""

EMPTY_SUCCESS = "Hello and Welcome to the best hangman game ever. \n\nGame Over \n"
DUMMY_SUCCESS = ""
HTTPS_SUCCESS = ""
SUCCESSES = [EMPTY_SUCCESS, DUMMY_SUCCESS, HTTPS_SUCCESS]


def test_integration():
    test_ui = TerminalUI()
    test_methods = [EmptyMethod()]
    # , DummyMethod(), HTTPSMethod()]
    test_games = [Game(test_ui, test_method) for test_method in test_methods]

    for test_index, test_game in enumerate(test_games):
        proc = subprocess.Popen(['python', '/Users/kbenarie/Projects/hangman-exercise/main.py'],
                                stdout=subprocess.PIPE)
        stdout = proc.stdout.read().decode('utf-8')
        assert stdout == SUCCESSES[test_index], '{} case did not succeed'.format(
            SUCCESSES[test_index])


def test_guess_letter():
    letters = ['a', 'd', 't', 'g', 'r']
