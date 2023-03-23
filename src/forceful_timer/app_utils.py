import subprocess

from difflib import SequenceMatcher

from forceful_timer.utils import os_type


def is_app_running(app_id: str) -> bool:
    """Check if a given app id is still running and return bool"""
    if os_type() == "linux":
        app_ids = [x.split()[0] for x in get_running_apps_raw()]
        return app_id in app_ids
    elif os_type() == "windows":
        raise NotImplementedError
    return False


def get_running_apps_raw() -> list:
    """Return list of app data

    This will be in form of a string: <id> <desktop> <user> <name>
    """
    if os_type() == "linux":
        decoded_output = subprocess.check_output(["wmctrl", "-l"])
        output = decoded_output.decode().split("\n")[:-1]
    elif os_type() == "windows":
        raise NotImplementedError
    return output


def extract_app_data_values(raw_app_data: str) -> tuple:
    """Filter out <id> and <name> from app data

    Given an app data: <id> <desktop> <user> <name> it returns (<id>, <name>).
    """
    app_data = list(filter(None, raw_app_data.split()))

    id_data = app_data[0]
    name_data = " ".join(app_data[3:])

    return (id_data, name_data)


def get_running_apps() -> list:
    """Return list of the currently running apps

    Each app is of format (<id>, <name>).
    """
    if os_type() == "linux":
        apps = [extract_app_data_values(x) for x in get_running_apps_raw()]
    elif os_type() == "windows":
        raise NotImplementedError
    return apps


def search_apps(app_name: str, apps: list) -> list:
    """Return list of apps that match the given app_name

    The returned list containts tuples of form: (<id>, <name>, <ratio>),
    where <ratio> is a float in [0, 1] that defines how well the app_name
    equals the name of the actual app.
    """
    matched_apps = [
        (a[0], a[1], SequenceMatcher(a=a[1], b=app_name).ratio()) for a in apps
    ]

    result_max_ratio = max(matched_apps, key=lambda x: x[2])
    result = [x for x in matched_apps if x[2] == result_max_ratio[2]]

    if result_max_ratio[2] < 0.5:
        raise ValueError("The given app doesn't match any running application.", result)
    return result


def get_apps(apps_to_find: list) -> list:
    """Return all apps that are running that match the given app

    The returned list contains tuples of form: (<id>, <name>, <ratio>),
    where <ratio> is how well they fit the given app.
    """
    running_apps = get_running_apps()
    found_apps = []
    for a in apps_to_find:
        found_apps.extend(search_apps(a, running_apps))
    return found_apps
