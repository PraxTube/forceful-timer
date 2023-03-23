import platform


def check_os():
    if os_type_str not in ["linux", "windows"]:
        raise OSError("Your operating system is not supported!", os_type_str)


os_type_str = platform.system().lower()
check_os()


def os_type():
    return os_type_str
