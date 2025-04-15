import inspect
import os
from .paths import cwdPath


def printDebug(*args):
    frame = inspect.currentframe().f_back  # 获取上一层调用栈
    relativeFileName = os.path.relpath(frame.f_code.co_filename, cwdPath)
    print(f"[{relativeFileName}:{frame.f_lineno}]", *args)
