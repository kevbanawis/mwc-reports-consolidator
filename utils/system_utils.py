from sys import version_info
from os import system


def display_system_info(month, day, year):
    system('cls')
    print(
        f'Date today: {month} {day}, {year}')
    print('System version: {}.{}.{}'.format(
        version_info[0], version_info[1], version_info[2]))
    print('')
