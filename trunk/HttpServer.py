#!/usr/bin/env python
import os
import sys
import Settings

from daemon import Daemon

def Main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "burn.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(['HttpServer.py', 'runserver', '%s:%s' % (Settings.HTTP_IPADDRESS,Settings.HTTP_PORT)])




if __name__ == "__main__":
    Main()