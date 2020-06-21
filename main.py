import json

import requests

API_URL = 'https://simpleapi.info/apps/numbers-info/info.php?results=json'


def find_phone_data(phone_number):
    """
    Get information about given phone number from the API.

    :param phone_number: The phone number to find data for.
    :return: Found items or an empty list.
    """
    response = requests.post(API_URL, data={'number': phone_number}, stream=True)
    response_converted = json.loads(response.content)

    return response_converted['items'] if 'yes' == response_converted['res'] else []


def main():
    """
    The main function that starts at startup.

    :return: Void.
    """

    print(' _   _                          _     _                      ')
    print('| \ | | ___  _ __ ___  _ __ ___| |__ (_)  ___ ___  _ __ ___  ')
    print('|  \| |/ _ \| \'_ ` _ \| \'__/ _ \ \'_ \| | / __/ _ \| \'_ ` _ \ ')
    print('| |\  | (_) | | | | | | | |  __/ |_) | || (_| (_) | | | | | |')
    print('|_| \_|\___/|_| |_| |_|_|  \___|_.__/|_(_)___\___/|_| |_| |_|')
    print('\n                                          Created By @ABGEO')

    phone = input('\nშეიყვანეთ მობილურის ნომერი: ')
    while '' != phone:
        items = find_phone_data(phone)
        if 0 != len(items):
            print('\nამ ნომერზე მოიძებნა შემდეგი მონაცემები:')
            for item in items:
                print('   - ' + item)
        else:
            print('\nჩანაწერი ამ ნომერზე ვერ მოიძებნა!')

        phone = input('\nშეიყვანეთ სხვა მობილურის ნომერი\nან დააჭირეთ Enter-ს დასასრულებლად: ')


if __name__ == '__main__':
    main()
