import os
import sys
from art import text2art


class UI:

    def __init__(self, subtitle=None):
        self.title = 'OGtweaker'
        self.subtitle = subtitle

    def print_title(self):
        if self.subtitle is None:
            print(text2art(self.title, font="small"), end='')
        else:
            print(text2art(self.title, font="small"), end='')
            print(self.subtitle, '\n')

    def print_message(self, message):
        os.system('cls')
        self.print_title()
        print(message, '\n')

    def append_message(self, message):
        print(message, '\n')

    def print_options(self, label, options, pointer=None):
        if label is not None:
            print(label, '\n')

        for option in options:
            if pointer == 'number':
                number = options.index(option) + 1
                print(f'[{number}] {option}')
            else:
                print(f'* {option}')
        print('')

    def get_numerical_choice(self, options):
        choice = None
        while not choice:
            try:
                user_input = int(input('Your choice: '))
                choice = (options[user_input - 1])
            except (IndexError, ValueError):
                print('There is no such option!', '\n')
        return choice

    def get_yes_or_no(self):
        while True:
            user_input = input('Your answer: ')
            answer = user_input.lower()
            if answer not in ['y', 'n']:
                print('Please answer with [y]es or [n]o!', '\n')
            else:
                break
        return answer

    def get_answer(self):
        while True:
            answer = input("Your answer: ")
            break
        return answer

# predefined menus
    def continue_menu(self):
        print('Do you want to continue? [y/n]', '\n')
        answer = self.get_yes_or_no()
        if answer == 'n':
            sys.exit(0)

    def list_continue_menu(self, label, points, pointer=None):
        os.system('cls')
        self.print_title()
        self.print_options(label, points, pointer)
        self.continue_menu()

    def yes_or_no_menu(self, question):
        os.system('cls')
        self.print_title()
        print(question + ' [y/n]', '\n')
        answer = self.get_yes_or_no()
        return answer

    def numeric_menu(self, label, options):
        os.system('cls')
        self.print_title()
        self.print_options(label, options, 'number')
        choice = self.get_numerical_choice(options)
        return choice

    def credits_menu(self, credits):
        self.print_message('All tweaks done!')
        self.print_options('Credits:', credits)
