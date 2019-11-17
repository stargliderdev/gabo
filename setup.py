from cx_Freeze import setup, Executable
import os, sys

packages = ["smtplib", "ssl"]
PYTHON_INSTALL_DIR = os.path.dirname(sys.executable)

include_files = [
    os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'libcrypto-1_1.dll'),
    os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'libssl-1_1.dll'),
    ".env", "message.txt"]

targetDir = "c:\\build\\"

setup(name="livros",
      version="2.0",
      description="Livros",
      executables=[Executable("main.py", base="Win32GUI", targetName="livros.exe",icon='books.ico')])
