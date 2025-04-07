"""Module to execute adb commands."""

import subprocess
from pathlib import Path
from time import sleep
from xml.etree import ElementTree


def run_adb_command(command: list) -> subprocess.CompletedProcess:
    """
    Executes an ADB (Android Debug Bridge) command using the subprocess module.

    Args:
        command (list): A list of strings representing the ADB command and its arguments.

    Returns:
        subprocess.CompletedProcess: The result of the executed command, containing
        information such as the return code, stdout, and stderr.

    Raises:
        subprocess.CalledProcessError: If the command exits with a non-zero status.
    """
    return subprocess.run(command, check=True, capture_output=True, text=True)


def pair(url: str, pairing_code: str) -> None:
    """
    Pairs an ADB (Android Debug Bridge) device using the provided URL and pairing code.

    Args:
        url (str): The IP address or hostname of the device to pair with, including the port (e.g., "192.168.1.100:5555").
        pairing_code (str): The pairing code required to authenticate the connection.

    Returns:
        None
    """
    command = ["adb", "pair", url, pairing_code]
    run_adb_command(command)


def extract(package_name: str, target: Path) -> None:
    """
    Extracts the APK file of a specified package from a connected Android device
    using ADB (Android Debug Bridge) and saves it to the target directory.

    Args:
        package_name (str): The name of the package whose APK is to be extracted.
        target (Path): The directory where the extracted APK file will be saved.

    Raises:
        RuntimeError: If the ADB command fails or the APK path cannot be determined.
    """
    command = ["adb", "shell", "pm", "path", package_name]
    result = run_adb_command(command)
    apk_path = result.stdout.strip().replace("package:", "").split("\n")[0]
    if apk_path:
        command = ["adb", "pull", apk_path, f"{target}/{package_name}.apk"]
        run_adb_command(command)


def connect(url: str) -> None:
    """
    Establishes a connection to a device using the Android Debug Bridge (ADB).

    Args:
        url (str): The URL or IP address of the device to connect to,
                   optionally including the port (e.g., "192.168.1.100:5555").

    Returns:
        None
    """
    command = ["adb", "connect", url]
    run_adb_command(command)


def is_connected() -> bool:
    """
    Checks if any devices are connected via ADB (Android Debug Bridge).

    This function runs the `adb devices` command to list all connected devices
    and their statuses. It parses the output to determine if any device is
    listed as "device", which indicates a successful connection.

    Returns:
        bool: True if at least one device is connected, False otherwise.
    """
    command = ["adb", "devices"]
    result = run_adb_command(command)
    deviceinfo_list = result.stdout.splitlines()[1:]
    return any("device" in deviceinfo for deviceinfo in deviceinfo_list)


def is_installed(package_name: str) -> bool:
    """
    Checks if a specific package is installed on an Android device.

    Args:
        package_name (str): The name of the package to check.

    Returns:
        bool: True if the package is installed, False otherwise.
    """
    command = ["adb", "shell", "pm", "list", "packages", package_name]
    result = run_adb_command(command)
    return package_name in result.stdout


def is_enabled(package_name: str) -> bool:
    """
    Checks if a specific package is enabled on an Android device.

    This function uses the `adb` command to list all enabled packages on the
    connected Android device and determines if the specified package is among them.

    Args:
        package_name (str): The name of the package to check.

    Returns:
        bool: True if the package is enabled, False otherwise.
    """
    command = ["adb", "shell", "pm", "list", "packages", "-e"]
    result = run_adb_command(command)
    return package_name in result.stdout


def install(apk_path: Path) -> None:
    """
    Installs an APK on a connected Android device using ADB.

    Args:
        apk_path (Path): The file path to the APK file to be installed.

    Returns:
        None
    """
    command = ["adb", "install", str(apk_path)]
    run_adb_command(command)


def clear_data(package_name: str) -> None:
    """
    Clears all data associated with the specified Android application package.

    This function uses the Android Debug Bridge (ADB) to execute the `pm clear` command,
    which removes all data (including cache, preferences, and databases) for the given
    application package on a connected Android device or emulator.

    Args:
        package_name (str): The package name of the Android application whose data
                            should be cleared (e.g., "com.example.app").

    Returns:
        None

    Raises:
        Any exceptions raised by the `run_adb_command` function will propagate.
    """
    command = ["adb", "shell", "pm", "clear", package_name]
    run_adb_command(command)


def uninstall(package_name: str) -> None:
    """
    Uninstalls the specified package from the connected Android device.

    This function attempts to uninstall the package for all users first.
    If that fails, it retries the uninstallation for the current user (user 0).

    Args:
        package_name (str): The package name of the application to uninstall.

    Returns:
        None

    Note:
        This function assumes that the `adb` command-line tool is properly
        configured and accessible from the system's PATH. It also relies on
        the `run_adb_command` function to execute the adb commands.
    """
    try:
        command = ["adb", "uninstall", package_name]
        run_adb_command(command)
    except:
        pass
    finally:
        command = ["adb", "uninstall", "--user", "0", package_name]
        run_adb_command(command)


def enable(package_name: str) -> None:
    """
    Enables the specified package on an Android device using the adb (Android Debug Bridge) command.

    Args:
        package_name (str): The name of the package to enable.

    Returns:
        None
    """
    command = ["adb", "shell", "pm", "enable", package_name]
    run_adb_command(command)


def disable(package_name: str) -> None:
    """
    Disables an Android package on a connected device using ADB (Android Debug Bridge).

    This function first attempts to uninstall the specified package. If the uninstallation
    fails or is skipped, it proceeds to disable the package for the current user.

    Args:
        package_name (str): The name of the Android package to disable.

    Returns:
        None

    Note:
        - Ensure that ADB is installed and properly configured on your system.
        - The connected Android device must have USB debugging enabled.
        - This function suppresses exceptions during the uninstallation process.
    """
    try:
        command = ["adb", "uninstall", package_name]
        run_adb_command(command)
    except:
        pass
    finally:
        command = ["adb", "shell", "pm", "disable-user", package_name]
        run_adb_command(command)


def tap(x: int, y: int) -> None:
    """
    Simulates a tap action on a connected Android device at the specified screen coordinates.

    Args:
        x (int): The x-coordinate of the screen where the tap should occur.
        y (int): The y-coordinate of the screen where the tap should occur.

    Returns:
        None
    """
    command = ["adb", "shell", "input", "tap", str(x), str(y)]
    run_adb_command(command)


def find_install_button() -> tuple[int, int] | None:
    """
    Attempts to locate the "Install" button on an Android device's UI using ADB and
    returns its center coordinates.

    This function uses the Android Debug Bridge (ADB) to dump the current UI hierarchy
    and parse it to find a button with the text "Install". If found, it calculates the
    center coordinates of the button's bounding box.

    Returns:
        tuple[int, int] | None: A tuple containing the (x, y) coordinates of the center
        of the "Install" button if found, or None if the button is not found after the
        specified number of attempts.

    Raises:
        xml.etree.ElementTree.ParseError: If the XML dump of the UI hierarchy is invalid.

    Notes:
        - The function retries up to `max_attempts` times, with a 1-second delay between
          attempts, to account for potential delays in the UI rendering.
        - The ADB commands used require proper permissions and a connected Android device.
    """
    max_attempts = 5
    for i in range(max_attempts):
        sleep(1)
        command = ["adb", "shell", "uiautomator", "dump"]
        run_adb_command(command)
        command = ["adb", "shell", "cat", "/sdcard/window_dump.xml"]
        result = run_adb_command(command)
        root = ElementTree.fromstring(result.stdout)
        nodes = root.findall(".//node")
        install_button = next(
            (node for node in nodes if node.attrib.get("text") == "Install"), None
        )
        if install_button is not None:
            break
    else:
        return None
    x1, y1, x2, y2 = map(
        int,
        install_button.attrib.get("bounds").replace("][", ",").strip("[]").split(","),
    )
    x = (x1 + x2) // 2
    y = (y1 + y2) // 2
    return (x, y)


def click_install_in_playstore():
    """
    Simulates a click on the "Install" button in the Play Store.

    This function locates the "Install" button by calling the `find_install_button`
    function, which returns the (x, y) coordinates of the button. It then simulates
    a tap action at the specified coordinates using the `tap` function.

    Returns:
        None
    """
    x, y = find_install_button()
    tap(x, y)


def navigate_playstore(package_name: str) -> None:
    """
    Launches the Google Play Store on the connected Android device and navigates
    to the details page of the specified app using its package name.

    Args:
        package_name (str): The package name of the app to navigate to in the Play Store.

    Returns:
        None
    """
    command = [
        "adb",
        "shell",
        "am",
        "start",
        "-a",
        "android.intent.action.VIEW",
        "-d",
        f"market://details?id={package_name}",
    ]
    run_adb_command(command)


def install_from_playstore(package_name: str) -> None:
    """
    Installs an application from the Google Play Store.

    This function navigates to the Play Store page of the specified package
    and initiates the installation process.

    Args:
        package_name (str): The package name of the application to be installed.

    Returns:
        None
    """
    navigate_playstore(package_name)
    click_install_in_playstore()
