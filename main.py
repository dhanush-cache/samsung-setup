from pathlib import Path
from time import sleep

import adb
from packages import to_freezze, to_install_from_playstore, to_uninstall


def connect():
    if not adb.is_connected():
        url = input("URL: ")
        adb.connect(url)
        if not adb.is_connected():
            print("Seems like the device isn't paired.")
            pairing_url = input("Pairing URL: ")
            code = input("Pairing code: ")
            adb.pair(pairing_url, code)
            adb.connect(url)


def freeze():
    for package in to_freezze:
        if not adb.is_enabled(package):
            continue
        print(f"Disabling: {package}...", end=" ")
        try:
            adb.clear_data(package)
            adb.disable(package)
        except:
            print("Failed!!!")
        else:
            print("Done!")


def uninstall():
    target = Path.home() / "sapps"
    target.mkdir(parents=True, exist_ok=True)
    for package in to_uninstall:
        if not adb.is_installed(package):
            continue
        print(f"Uninstalling: {package}...", end=" ")
        try:
            adb.clear_data(package)
            adb.extract(package, target)
            adb.uninstall(package)
        except:
            print("Failed!!!")
        else:
            print("Done")


def install_from_playstore():
    for package in to_install_from_playstore:
        if adb.is_installed(package):
            continue
        print(f"Installing: {package}...", end=" ")
        try:
            adb.install_from_playstore(package)
        except:
            print("Failed!!!")
        else:
            print("Done")


def main():
    connect()
    freeze()
    uninstall()
    install_from_playstore()


if __name__ == "__main__":
    main()
