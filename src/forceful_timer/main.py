import subprocess
import argparse
import time
import signal

from tqdm import tqdm
import chime

from forceful_timer import app_utils
from forceful_timer import ui_utils
from forceful_timer.utils import os_type


parser = argparse.ArgumentParser(
    description="Shut down the system after the given time period."
)
parser.add_argument(
    "minutes",
    nargs="?",
    action="store",
    type=int,
    default=60,
    help="time in minutes till shutdown",
)
parser.add_argument(
    "-a",
    "--app",
    action="append",
    type=str,
    default=[],
    help="the app that will get closed if the timer is interrupted",
)
parser.add_argument(
    "-l",
    "--list-apps",
    action="store_true",
    help="list all running applications and exit.",
)
parser.add_argument(
    "--sound-theme",
    action="store",
    type=str,
    default="chime",
    choices=["big-sur", "chime", "mario", "material", "pokemon", "sonic", "zelda"],
    help="the theme to use to play sounds, see chime",
)
args = parser.parse_args()


def handler(sig, frame):
    print("\nCtrl + Z pressed, ignoring it.")


signal.signal(signal.SIGTSTP, handler)


def shutdown():
    if os_type() == "linux":
        subprocess.call(["shutdown", "now"])
    elif os_type() == "windows":
        subprocess.call(["shutdown", "/s", "/t", "0"])


def cancel_shutdown(apps):
    print("Shutdown cancled.\n")

    for app in apps:
        if app_utils.is_app_running(app[0]):
            subprocess.call(["wmctrl", "-i", "-c", app[0]])
            print("Terminating: {}".format(app))
        else:
            print("Skipping app, because it's not running anymore: {}".format(app))


def check_remaining_seconds(remaining_seconds):
    if remaining_seconds <= 15:
        chime.warning()
    elif 29 <= remaining_seconds <= 31:
        chime.info()


def loop():
    seconds = args.minutes * 60
    for i in tqdm(range(seconds), desc="Shutting down in"):
        check_remaining_seconds(seconds - i)
        time.sleep(1)


def set_up(apps):
    chime.notify_exceptions()
    chime.theme(args.sound_theme)

    ui_utils.clear_terminal()
    ui_utils.print_title()
    ui_utils.print_apps(apps)


def main():
    if args.list_apps:
        ui_utils.print_running_apps()
        exit()

    apps = app_utils.get_apps(args.app)
    set_up(apps)

    try:
        loop()
    except KeyboardInterrupt:
        ui_utils.clear_terminal()
        cancel_shutdown(apps)
        exit()
    except Exception as err:
        raise err

    shutdown()


if __name__ == "__main__":
    main()
