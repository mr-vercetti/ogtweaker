import sys
from ui import UI
from mohaa.mohaa import Mohaa
from gtavc.gtavc import Gtavc


def main():
    ui = UI()
    
    main_option = ui.numeric_menu(
        'Welcome to OGtweaker!',
        [
            'MoH Allied Assault',
            'Grand Theft Auto Vice City',
            'Exit'
            ])

    if main_option == 'Exit':
        sys.exit(0)
    elif main_option == 'MoH Allied Assault':
        mohaa = Mohaa()
        mohaa.main()
    elif main_option == 'Grand Theft Auto Vice City':
        gtavc = Gtavc()
        gtavc.main()


if __name__ == "__main__":
    main()
