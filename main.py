from constants import date_formats
from process.reportconsolidation import ReportConsolidation
from utils.file_handling import (
    is_path_exists, is_file_open,
    conditional_exit, get_current_path,
    exit_app
)
from utils.system_utils import display_system_info
import subprocess
import time
from operator import itemgetter


class Main():

    # public variables
    mwc_meta_paths = {}
    lawc_meta_paths = {}

    def __init__(self):
        self.set_report_path()

    def _script_selector(self, p):
        return r'{}'.format(
            get_current_path(r'bats\{}.bat').format(
                {1: 'mwc', 2: 'lawc'}.get(p)
            )
        )

    def set_report_path(self):

        mwc_paths, lawc_paths = itemgetter('mwc_paths', 'lawc_paths')(
            self.get_config_values()
        )

        set_paths = (
            (mwc_paths, self.mwc_meta_paths, 'mwc'),
            (lawc_paths, self.lawc_meta_paths, 'lawc')
        )

        for path_config, set_path_var, process_type in set_paths:

            for item, value in path_config.items():

                if not (len(value.split(',')) > 1):
                    for name, date_value in date_formats.__all__.items():
                        value = str(value).replace(
                            f'${str(name)}', str(date_value)
                        )
                else:
                    value = value.split(',')
                set_path_var.update({item: value})

    def get_config_values(self):
        from configparser import ConfigParser

        cfg = ConfigParser()
        cfg.read('config.ini')

        return dict(
            mwc_paths=cfg['mwc'],
            lawc_paths=cfg['lawc']
        )

    def get_user_input(self) -> int:
        return int(input('Choose process to consolidate *\n1. MWC\n2. LAWC\n3. Exit\nCHOICE [1-3]: ').strip())

    def get_process(self):
        return {
            1: self.mwc_meta_paths,
            2: self.lawc_meta_paths,
        } \
            .get(self.get_user_input(), None)

    def runscript(self, p) -> bool:
        is_successful = False
        try:
            print(
                f'\n[{"MWC" if p == 1 else "LAWC"}] -> Transfering generated files to FTP ...')
            if subprocess.check_call([self._script_selector(p)]) == 0:
                is_successful = True
        except Exception as e:
            print(f'\nScript Error: {e}'.format())
        return is_successful


if __name__ == '__main__':

    display_system_info(
        date_formats.month_word,
        date_formats.current_date,
        date_formats.current_year,
    )
    while True:

        m = Main()

        process = m.get_process()
        conditional_exit(lambda process: not process, [
            process], 'Exit triggered by User.')

        consolidate_report = ReportConsolidation(process)
        dunning_path = consolidate_report.dunning_path
        dunning_filename = consolidate_report.dunning_filename

        conditional_exit(
            is_path_exists, [dunning_path],
            f'\n[PATH ERROR]: Path does not exists: `{dunning_path}`'
        )

        conditional_exit(
            is_file_open, [dunning_filename],
            f"""[FILE ERROR]: Please close the file to avoid error: {dunning_filename}"""
        )

        if m.runscript(process['process_type']):
            start = time.time()
            consolidate_report.execute_process()
            end = time.time()
            print('Process Time: {} seconds'.format(
                str(round(float(end - start), 2))))
        else:
            print('Script not completed. Check Above Logs.')

        time.sleep(0.1)
        ch = input('\nAnother run? [y/n]: ').strip().lower()
        if ch == 'y':
            continue
        else:
            exit_app()
