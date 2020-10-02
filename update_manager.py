"""
Update Manager.
"""

import json
import os
import subprocess
import sys

import requests
from packaging import version

from nomrebi import (
    __version__, Colors
)

REPO = 'ABGEO/nomrebi-py'


def get_latest_release():
    """
    Get latest release from the GitHub API.

    :return: Response from the GitHub API.
    """
    response = requests.get(f'https://api.github.com/repos/{REPO}/releases/latest')

    return json.loads(response.content)


def process_update():
    """
    Update (git pull) project.

    :return: Void.
    """

    try:
        subprocess.check_output('git pull', stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
    except Exception:
        print(f'\nUnable to update application. Try to manually "git pull" or '
              f'"git clone" this repository: https://github.com/{REPO}')
    else:
        # Restart.
        os.execl(sys.executable, sys.executable, *sys.argv)


def check_update():
    """
    Compare current version to latest one and run update function if needed.

    :return: Void.
    """

    latest_release = get_latest_release()
    latest_version = latest_release['tag_name']

    if version.parse(latest_version) > version.parse(__version__):
        print(f'Version {Colors.OKGREEN}{latest_version}{Colors.ENDC} is available '
              f'(Current version is {Colors.OKGREEN}{__version__}{Colors.ENDC}. Update notes: ')

        print(latest_release['body'])

        if input(f'Update to version {Colors.OKGREEN}{latest_version}{Colors.ENDC}? [Y/n] ') in ['Y', 'y']:
            process_update()
