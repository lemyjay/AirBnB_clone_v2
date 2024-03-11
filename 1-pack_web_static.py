#!/usr/bin/python3
"""
A Fabric script that generates a .tgz archive from the contents of the
web_static folder of the AirBnB Clone repo using the do_pack function.
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    # Create the folder 'versions' if it doesn't exist
    local("mkdir -p versions")

    # Create the name of the archive with the current date and time
    now = datetime.now()
    file_name = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second)

    # Compress the contents of the web_static folder into a .tgz archive
    result = local("tar -cvzf {} web_static".format(file_name))

    # Check if the archive has been correctly generated
    if result.failed:
        return None
    return file_name
