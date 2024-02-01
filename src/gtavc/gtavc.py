from tweaker import Tweaker
from ui import UI


class Gtavc:

    def __init__(self):
        self.game = 'Grand Theft Auto Vice City'
        self.exe_file = 'gta-vc.exe'

    def main(self):
        ui = UI(self.game)
        tweaker = Tweaker(self.game, self.exe_file)
        config = tweaker.load_config()
        download_url = config['download_url']
        game_dir = tweaker.get_game_dir_auto()
        screen_width, screen_height = tweaker.get_resolution()
        temp_dir = tweaker.get_tempdir()

        tweaks = [
            "Downgrade exe to 1.0",
            "Add widescreen support",
            "Set native resolution",
            "Lock FPS at 60",
            "Fix common graphic and gameplay issues",
            "Improve draw distance",
            "Add proper controller support",
            "Make NPCs more talktative, like in PS2 version"
            "Add graphic effects from PS2 and Xbox (optional)",
            "Improve LOD (optional)",
            "HD intro movies (optional)"
        ]

        credits = [
            "SilentPatch, DDraw - Silent (https://cookieplmonster.github.io)",
            "Ultimate-ASI-Loader, WidescreenFix, LimitAdjuster, Project2DFX - ThirteenAG (https://github.com/ThirteenAG)",
            "SkyGFX, sharptrails - aap (https://github.com/aap)",
            "rundll32.exe fix - Swoorup",
            "PedSpeech - Sergeanur (https://github.com/Sergeanur)"
        ]

        ui.list_continue_menu(
            'List of tweaks that OGtweaker will perform:',
            tweaks)

        tweaker.download_unzip(
            f'{download_url}/gtavc/gtavc-base-tweaks.zip',
            f'{temp_dir}\\gtavc-base-tweaks.zip',
            game_dir)

        update_resolution = {
            'MAIN': {
                'ResX': screen_width,
                'ResY': screen_height,
            }
        }

        tweaker.edit_ini(
            f'{game_dir}\\scripts\\GTAVC.WidescreenFix.ini',
            update_resolution)

        skygfx_answer = ui.yes_or_no_menu(
            'Do you want to install SkyGFX mod (graphic effects from consoles)?')
        if skygfx_answer == 'y':
            tweaker.download_unzip(
                f'{download_url}/gtavc/gtavc-skygfx.zip',
                f'{temp_dir}\\gtavc-base-tweaks.zip',
                game_dir)

        project2dfx_answer = ui.yes_or_no_menu(
            'Do you want to install Project2DFX mod (LOD improvement)?')
        if project2dfx_answer == 'y':
            tweaker.download_unzip(
                f'{download_url}/gtavc/gtavc-project2dfx.zip',
                f'{temp_dir}\\gtavc-project2dfx.zip',
                game_dir)

        hdintro_answer = ui.yes_or_no_menu(
            'Do you want to install HD intro movies?')
        if hdintro_answer == 'y':
            tweaker.download_unzip(
                f'{download_url}/gtavc/gtavc-hd-intro.zip',
                f'{temp_dir}\\gtavc-hd-intro.zip',
                game_dir)

        ui.credits_menu(credits)