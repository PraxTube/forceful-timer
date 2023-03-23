import os
import subprocess

from forceful_timer.utils import os_type
from forceful_timer.app_utils import get_running_apps


def clear_terminal():
    if os_type() == "linux":
        subprocess.run("clear", shell=True)
    elif os_type() == "windows":
        subprocess.run("cls", shell=True)


def get_title() -> list:
    """Read the lines from title.txt and return them

    The returned list contains strings.
    """
    path = os.path.join(os.path.dirname(__file__), "title.txt")
    with open(path) as f:
        title = f.readlines()
    return title


def print_title():
    for line in get_title():
        print(line.replace("\n", ""))


def print_apps(apps):
    for a in apps:
        print("Going to close: {}".format(a))


def print_running_apps():
    running_apps = get_running_apps()
    for a in running_apps:
        print(a)
