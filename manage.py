#!/usr/bin/env python
# ENV:
# C:\Users\Ronnie\Envs\p27\Scripts\python;C:\Users\Ronnie\Envs\p27\Scripts;C:\Users\Ronnie\AppData\Local\atom\bin;

import os
import sys

if __name__ == "__main__":
    #print sys.argv
    #if len(sys.argv)>(2):
    #    sys.argv = sys.argv[:-2]
    #print sys.argv
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beauticart.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
