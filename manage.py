#!/usr/bin/env python

import os
import sys


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bojv4.settings")

    from django.core.management import execute_from_command_line
    import sys

    reload(sys)

    sys.setdefaultencoding('utf-8')

    execute_from_command_line(sys.argv)
