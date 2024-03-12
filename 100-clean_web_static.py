#!/usr/bin/python3
"""
Fabric script (based on the file 3-deploy_web_static.py) that deletes
out-of-date archives
"""
from fabric.api import *
from datetime import datetime
import os

env.hosts = ['web1.lemyjay.tech', 'web2.lemyjay.tech']


def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    try:
        number = int(number)
        if number < 0:
            number = 0
    except ValueError:
        number = 0

    number += 1
    local_path = "./versions"
    remote_path = "/data/web_static/releases"
    with lcd(local_path):
        local_archives = sorted(os.listdir("."), reverse=True)
        for archive in local_archives[number:]:
            local("rm -f {}".format(archive))

    with cd(remote_path):
        run_archives = run("ls -1tr").split("\n")
        for archive in run_archives[number:]:
            run("rm -rf {}".format(archive))
