#!/usr/bin/env python

"""
Get information about phone numbers stored in the Nomrebi.com database
"""

import json
import signal

import requests

import update_manager as um

__author__ = "Temuri Takalandze"
__copyright__ = "Copyright 2020, Temuri Takalandze"
__credits__ = ["Temuri Takalandze"]
__license__ = "MIT"
__version__ = "1.6.0"
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


def find_phone_data(phone_number, u_phone, u_id, u_token):
    """
    Get information about given phone number from the API.

    :param phone_number: The phone number to find data for.
    :param u_phone: User phone number.
    :param u_id: User ID.
    :param u_token: User auth Token.
    :return: Found items or an empty list.
    """
    response = requests.get(API_BASE_URL + '/number-info/' + phone_number,
                            params={'u_phone': u_phone, 'u_id': u_id, 'u_token': u_token})

    return json.loads(response.content)


def authenticate():
    """
    Make an authentication request the API.
    :return: Authentication data.
    """

    u_phone = input('აპლიკაციით სარგებლობისთვის შეიყვანეთ თქვენი ტელეფონის ნომერი: ')
    response = requests.get(API_BASE_URL + '/authenticate/' + u_phone)
    response = json.loads(response.content)

    if response['authenticated']:
        response['data']['phone'] = u_phone
        return response['data']

    if response['sms_sent']:
        sms_code = input('შეიყვანეთ მიღებული SMS კოდი: ')

        response = requests.get(API_BASE_URL + '/authenticate/' + u_phone + '/sms/' + sms_code)
        response = json.loads(response.content)

        if response['valid']:
            response['data']['phone'] = u_phone
            return response['data']

    return {None, None, None}


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
    print("\n")

    u_id, u_token, u_phone = authenticate().values()
    phone = input('\nშეიყვანეთ მოსაძებნი მობილურის ნომერი: ')

    while '' != phone:
        print(f'\n{Colors.HEADER}მიმდინარეობს მონაცემების ძიება... დაელოდეთ\n{Colors.ENDC}')
        items = find_phone_data(phone, u_phone, u_id, u_token)
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
