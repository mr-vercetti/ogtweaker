import sys
from ui import UI
from mohaa.mohaa import Mohaa


def main():
    ui = UI()
    
    main_option = ui.numeric_menu(
        'Welcome to OGtweaker!',
        [
            'MoH Allied Assault',
            'Exit'
            ])

    if main_option == 'Exit':
        sys.exit(0)
    elif main_option == 'MoH Allied Assault':
        mohaa = Mohaa()
        mohaa.main()


if __name__ == "__main__":
    main()
