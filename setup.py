import sys
from cx_Freeze import setup, Executable


if sys.platform =="win32":
    base = "win32GUI"

setup(name="puzzle",
      version="1.0",
      description="bla",
      options={'build_exe': {'include_files': include_files}},
      executables=[Executable("client.py", base=base)])
