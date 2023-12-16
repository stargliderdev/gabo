import os
import subprocess
import sys
import platform
import time

import parameters as gl


def get_system_info(show=False):
    os_name = platform.system()
    os_version = platform.version()
    hostname = platform.node()
    architecture = platform.architecture()
    python_version = platform.python_version()
    gl.RUN_FROM = os.path.dirname(os.path.abspath(__file__))

    # Print the information
    if show:
        print('{:>18}'.format("Operating System:"), os_name)
        print('{:>18}'.format("      OS Version:"), os_version)
        print('{:>18}'.format("        Hostname:"), hostname)
        print('{:>18}'.format("    Architecture:"), architecture[0] , architecture[1])
        print('{:>18}'.format("  Python Version:"), python_version)
        print('{:>18}'.format("        Run From:"), gl.RUN_FROM)

    if os_name == 'Windows':
        import ctypes
        gl.DOCUMENTS_DIR = os.path.expanduser('~\\Documents')
        # print('{:>18}'.format('Documentos:'), gl.DOCUMENTS_DIR)
        user32 = ctypes.windll.user32
        SM_CXSCREEN = 0
        SM_CYSCREEN = 1
        # Retrieve screen resolution
        gl.SCREEN_WIDTH = user32.GetSystemMetrics(SM_CXSCREEN)
        gl.SCREEN_HEIGHT = user32.GetSystemMetrics(SM_CYSCREEN)
        # print('{:>18}'.format('W Screen:'), gl.SCREEN_WIDTH)
        # print('{:>18}'.format('H Screen:'), gl.SCREEN_HEIGHT)


def install_dependencies(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def main():
    get_system_info()
    try:
        from PyQt5.QtWidgets import QDesktopWidget
        run_main = lambda: os.system('python.exe main.py')
        run_main ()
        exit()
    except (ImportError, ModuleNotFoundError):
        clear = lambda: os.system('cls')
        clear()
        pip_update = lambda: os.system('python.exe -m pip install --upgrade pip')
        pip_update()
        install_dependencies('pyqt5')
        install_dependencies('pyqtwebengine')
        time.sleep(1)
        run_main = lambda: os.system('python.exe main.py')
        run_main ()
        exit(0)

if __name__ == '__main__':
    main()
