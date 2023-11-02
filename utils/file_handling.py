from os import path, chdir, system
from sys import exit, _MEIPASS


def is_path_exists(current_path) -> bool:
    return not path.exists(current_path)


def is_file_open(path, filename) -> bool:
    file = path + filename
    try:
        open(file, 'r+')
        return False
    except IOError:
        return True


def conditional_exit(fn, params, error_message):
    if fn(*params):
        print(error_message)
        exit_app()


def exit_app(): exit(0)


def change_working_dir(file_path): chdir(f'{file_path}')
def run_system_command(sys_command): system(sys_command)


def get_current_path(relative_path):
    try:
        base_path = _MEIPASS
    except Exception:
        base_path = path.abspath('.')

    return path.join(base_path, relative_path)
