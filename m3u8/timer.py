''' timer.py - calculate the time of a Python program's execution.

Ref:

[How do I get time of a Python program's execution?](https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution)

Usage:
    t = timing()
    t("... {}".format(running_python_program)

'''


import time

def timing():
    start_time = time.time()
    return lambda x: print("[{:.5f}s] {}".format(time.time() - start_time, x))