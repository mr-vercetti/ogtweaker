import inspect
from tweaker import Tweaker
from ui import UI


class Mohaa:

    def __init__(self):
        self.game = 'MoH Allied Assault'
        self.exe_file = 'MOHAA.exe'

    def main(self):
        ui = UI(self.game)
        tweaker = Tweaker(self.game, self.exe_file)
        config = tweaker.load_config()
        download_url = config['download_url']
        game_dir = tweaker.get_game_dir_auto()
        screen_width, screen_height = tweaker.get_resolution()
        temp_dir = tweaker.get_tempdir()
        main_game_dir = f'{game_dir}\\main'
        # dlcs
        spearhead_dir = f'{game_dir}\\mainta'
        breakthrough_dir = f'{game_dir}\\maintt'
        spearhead = tweaker.check_path_exists(f'{spearhead_dir}')
        breakthrough = tweaker.check_path_exists(f'{breakthrough_dir}')

        tweaks = [
            'Set max quality graphics settings',
            'Set native resolution',
            'Improve mouse responsiveness',
            'Increase frame limit',
            'Enable in-game console (optional)',
            'Change default FOV (optional, download required)',
            'Install HD textures mod (optional, download required)'
        ]

        credits = [
            'djibe89, [EOI]MoLoCh, [EOI]SuB-0, [EOI]b0x - MoHAA HD textures mod',
            'WSGF community - MoHAA FOV files'
        ]

        ui.list_continue_menu(
            'List of tweaks that OGtweaker will perform:',
            tweaks)

        console_answer = ui.yes_or_no_menu(
            'Do you want to enable in-game console?')
        if console_answer == 'y':
            console_value = 1
        else:
            console_value = 0

        tweak_config = inspect.cleandoc(f'''
            seta cg_drawviewmodel "2"
            seta cg_effectdetail "1.0"
            seta cg_marks_add "1"
            seta cg_max_tempmodels "1200"
            seta cg_rain "1"
            seta cg_reserve_tempmodels "240"
            seta cg_shadows "2"
            seta g_ddayfodderguys "2"
            seta g_ddayfog "0"
            seta g_ddayshingleguys "2"
            seta r_colorbits "32"
            seta r_drawstaticdecals "1"
            seta r_ext_compressed_textures "1"
            seta r_fastdlights "0"
            seta r_fastentlight "0"
            seta r_forceClampToEdge "1"
            seta r_lodcap "1.0"
            seta r_lodscale "1.1"
            seta r_lodviewmodelcap "1.0"
            seta r_maxmode "9"
            seta r_picmip "0"
            seta r_picmip_models "0"
            seta r_picmip_sky "0"
            seta r_subdivisions "3"
            seta r_texturebits "32"
            seta r_texturemode "GL_LINEAR_MIPMAP_LINEAR"
            seta r_vidmode1024 "0"
            seta r_vidmodemax "1"
            seta s_khz "44"
            seta ter_error "4"
            seta ter_maxlod "6"
            seta ter_maxtris "24576"
            seta vss_draw "1"
            seta vss_maxcount "15"
            seta r_uselod "0"
            seta in_mouse "-1"
            seta m_filter "1"
            seta sensitivity "10.500000"
            seta g_lastsave "m1l2a0001"
            seta r_customwidth "{screen_width}"
            seta r_customheight "{screen_height}"
            seta r_mode "-1"
            seta r_gamma "1.000000"
            seta r_texturemode "GL_LINEAR_MIPMAP_NEAREST"
            seta g_subtitle "1"
            seta ui_console "{console_value}"''')

        tweaker.write_to_file(
            f'{main_game_dir}\\autoexec.cfg',
            tweak_config)

        if spearhead is True:
            tweaker.write_to_file(
                f'{spearhead_dir}\\autoexec.cfg',
                tweak_config)

        if breakthrough is True:
            tweaker.write_to_file(
                f'{breakthrough_dir}\\autoexec.cfg',
                tweak_config)

        fov_answer = ui.yes_or_no_menu(
            'Do you want to change default FOV?')
        if fov_answer == 'y':
            fov_value = ui.numeric_menu(
                'Choose the FOV value that you prefer:',
                ['90', '100', '110', '120', '130', '140', '150'])

            tweaker.download_unzip(
                f'{download_url}/mohaa/mohaa-fov.zip',
                f'{temp_dir}\\mohaa-fov.zip',
                temp_dir)

            tweaker.copy(
                f'{temp_dir}\\mohaa-fov\\{fov_value}\\gamex86.dll',
                main_game_dir)

            if spearhead is True:
                tweaker.copy(
                    f'{temp_dir}\\mohaa-fov\\spearhead\\{fov_value}\\gamex86.dll',
                    spearhead_dir)

            if breakthrough is True:
                tweaker.copy(
                    f'{temp_dir}\\mohaa-fov\\breakthrough\\{fov_value}\\gamex86.dll',
                    breakthrough_dir)

            tweaker.remove(f'{temp_dir}\\mohaa-fov')

        hd_textures_answer = ui.yes_or_no_menu(
            'Do you want to download and install HD textures mod?')
        if hd_textures_answer == 'y':
            tweaker.download_unzip(
                f'{download_url}/mohaa/mohaa-hd-textures.zip',
                f'{temp_dir}\\mohaa-hd-textures.zip',
                main_game_dir)

        ui.credits_menu(credits)
