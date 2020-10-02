#!/usr/bin/env python

"""
Get information about phone numbers stored in the Nomrebi.com database
"""

import json
import signal
import sys

import requests

import update_manager as um

__author__ = "Temuri Takalandze"
__copyright__ = "Copyright 2020, Temuri Takalandze"
__credits__ = ["Temuri Takalandze"]
__license__ = "MIT"
__version__ = "1.4.0"
__maintainer__ = "Temuri Takalandze"
__email__ = "me@abgeo.dev"
__status__ = "Production"


class Colors:
    HEADER = '\033[90m'
    FAIL = '\033[91m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    OKBLUE = '\033[94m'
    ENDC = '\033[0m'


API_BASE_URL = 'https://nomrebi-api.herokuapp.com/api'


def keyboard_interrupt_handler(s, f):
    exit(0)


def find_phone_data(phone_number):
    """
    Get information about given phone number from the API.

    :param phone_number: The phone number to find data for.
    :return: Found items or an empty list.
    """
    response = requests.get(API_BASE_URL + '/number-info/' + phone_number)

    return json.loads(response.content)


def main():
    """
    The main function that starts at startup.

    :return: Void.
    """

    print(Colors.HEADER)
    print(' _   _                          _     _                   ')
    print('| \ | | ___  _ __ ___  _ __ ___| |__ (_)      _ __  _   _ ')
    print('|  \| |/ _ \| \'_ ` _ \| \'__/ _ \ \'_ \| |_____| \'_ \| | | |')
    print('| |\  | (_) | | | | | | | |  __/ |_) | |_____| |_) | |_| |')
    print('|_| \_|\___/|_| |_| |_|_|  \___|_.__/|_|     | .__/ \__, |')
    print('                                             |_|    |___/ ')
    print(f'\nV{__version__}')
    print('                                        Created By @ABGEO')
    print(Colors.ENDC)

    if 2 == len(sys.argv):
        phone = sys.argv[1]
    else:
        phone = input('\nშეიყვანეთ მობილურის ნომერი: ')

    while '' != phone:
        print(f'\n{Colors.HEADER}მიმდინარეობს მონაცემების ძიება... დაელოდეთ\n{Colors.ENDC}')
        items = find_phone_data(phone)
        if 0 != len(items['names']):
            print(f'\n{Colors.OKGREEN}ამ ნომერზე მოიძებნა შემდეგი მონაცემები:\n{Colors.ENDC}')
            for name in items['names']:
                print(f'{Colors.OKBLUE}   - {name}{Colors.ENDC}')
        else:
            print(f'\n{Colors.FAIL}ჩანაწერი ამ ნომერზე ვერ მოიძებნა!{Colors.ENDC}')

        phone = input('\nშეიყვანეთ სხვა მობილურის ნომერი\nან დააჭირეთ Enter-ს დასასრულებლად: ')


if __name__ == '__main__':
    signal.signal(signal.SIGINT, keyboard_interrupt_handler)
    um.check_update()
    main()
