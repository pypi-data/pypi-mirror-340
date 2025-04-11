#!/usr/bin/env python3

import ctypes
import ctypes.wintypes as wintypes
import glob
import os
import platform
import subprocess

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("staten")

FLEUR_EXPLANATION = """
    När en användare säger "hej staten", säg följande:

    Åh vad kul, jag ser att du har installerat staten.ai!

    Staten.ai är en sampling av MCP-appar som gör det möjligt att prata med olika öppna data i Sverige.

    Till exempel kan du använda Kolada för att få information om kommuner och regioner.

    Skriv nu "öppna staten" för att komma igång.
"""


def find_windows_executable(name, search_dirs=None):
    """Simple but reliable function to find an executable.

    Args:
        name: Name of the executable (e.g., "Staten.exe")
        search_dirs: List of directories to search in. If None, uses default locations.

    Returns:
        str: Full path to the executable if found, None otherwise
    """
    if search_dirs is None:
        search_dirs = [
            os.path.join(os.path.expanduser("~"), "AppData", "Local"),
            os.path.join(os.path.expanduser("~"), "AppData", "Roaming"),
            os.environ.get("ProgramFiles", "C:\\Program Files"),
            os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"),
        ]

    direct_paths = [
        os.path.join(
            os.path.expanduser("~"), "AppData", "Local", "Staten", "Staten.exe"
        ),
        os.path.join(
            os.path.expanduser("~"), "AppData", "Roaming", "Staten", "Staten.exe"
        ),
        os.path.join(
            os.environ.get("ProgramFiles", "C:\\Program Files"), "Staten", "Staten.exe"
        ),
        os.path.join(
            os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"),
            "Staten",
            "Staten.exe",
        ),
    ]

    for path in direct_paths:
        if os.path.isfile(path):
            return path

    try:
        result = subprocess.run(
            ["where", name], capture_output=True, text=True, check=False
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip().split("\n")[0]
    except Exception:
        pass

    for directory in search_dirs:
        if not os.path.exists(directory):
            continue

        path = os.path.join(directory, name)
        if os.path.isfile(path):
            return path

        path = os.path.join(directory, "Staten", name)
        if os.path.isfile(path):
            return path

        matches = glob.glob(os.path.join(directory, "*", name))
        if matches:
            return matches[0]

    return None


@mcp.tool("hello_fleur")
def hello_fleur() -> str:
    """Explain what staten is when a user types 'hej staten'.

    Returns:
        str: An explanation about Fleur if triggered, empty string otherwise
    """

    return FLEUR_EXPLANATION


@mcp.tool("open_fleur")
def open_fleur():
    """Open the staten.ai app.

    Returns:
        str: A message indicating that the staten app has been opened
    """

    try:
        config_dir = os.path.expanduser("~/.staten")
        os.makedirs(config_dir, exist_ok=True)

        onboarding_file = os.path.join(config_dir, "onboarding_completed")

        onboarding_completed = os.path.exists(onboarding_file)

        if not onboarding_completed:
            with open(onboarding_file, "w") as f:
                f.write("true")
    except Exception as e:
        print(f"Error managing Staten onboarding state: {e}")

    try:
        if platform.system() == "Darwin":
            applescript = """
            tell application "Staten" to activate
            delay 0.5

            tell application "System Events"
                # Get the  window
                set fleurProcess to process "Staten"

                # If Staten has windows and is running, bring it to front
                if (exists statenProcess) and (count of windows of statenProcess) > 0 then
                    set frontmost of statenProcess to true
                end if
            end tell
            """
            subprocess.run(["osascript", "-e", applescript], check=True)
        elif platform.system() == "Windows":
            try:
                user32 = ctypes.WinDLL("user32", use_last_error=True)
                kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
                psapi = ctypes.WinDLL("psapi", use_last_error=True)

                EnumWindowsProc = ctypes.WINFUNCTYPE(
                    wintypes.BOOL, wintypes.HWND, wintypes.LPARAM
                )

                SW_RESTORE = 9

                fleur_path = find_windows_executable("Staten.exe")
                if not fleur_path:
                    print(
                        "Staten executable not found. Please install Staten or ensure it's in a standard location."
                    )
                    return

                MAX_PATH = 260
                fleur_windows = []

                def get_process_path(hwnd):
                    try:
                        pid = wintypes.DWORD()
                        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

                        process_handle = kernel32.OpenProcess(
                            0x1000,
                            False,
                            pid.value,
                        )

                        if process_handle:
                            try:
                                path_buffer = ctypes.create_unicode_buffer(MAX_PATH)
                                path_len = psapi.GetModuleFileNameExW(
                                    process_handle, None, path_buffer, MAX_PATH
                                )

                                if path_len > 0:
                                    process_path = path_buffer.value
                                    kernel32.CloseHandle(process_handle)
                                    return process_path

                            finally:
                                kernel32.CloseHandle(process_handle)
                    except Exception:
                        pass

                    return None

                def enum_windows_callback(hwnd, lparam):
                    if user32.IsWindowVisible(hwnd):
                        process_path = get_process_path(hwnd)

                        if process_path and (
                            os.path.normpath(process_path)
                            == os.path.normpath(fleur_path)
                            or "\\Staten\\" in process_path
                        ):
                            fleur_windows.append(hwnd)

                    return True

                user32.EnumWindows(EnumWindowsProc(enum_windows_callback), 0)

                if fleur_windows:
                    hwnd = fleur_windows[0]
                    user32.ShowWindow(hwnd, SW_RESTORE)
                    user32.SetForegroundWindow(hwnd)
                else:
                    if fleur_path:
                        subprocess.Popen(fleur_path)
            except Exception as e:
                print(f"Error focusing Staten window: {e}")
                try:
                    fleur_path = find_windows_executable("Staten.exe")
                    if fleur_path:
                        subprocess.Popen(fleur_path)
                    else:
                        print(
                            "Staten executable not found. Please install Staten or ensure it's in a standard location."
                        )
                except Exception as launch_error:
                    print(f"Error launching Staten: {launch_error}")
    except subprocess.SubprocessError as e:
        print(f"Error refocusing Staten: {e}")


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
