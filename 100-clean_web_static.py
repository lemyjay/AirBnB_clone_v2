#!/usr/bin/python3
"""
A Fabric script that distributes the archive to the web
servers using do_deploy function.
"""

from fabric.api import local, env, put, run
import os.path
from datetime import datetime

# Define the list of web servers
env.hosts = ['100.25.0.107', '100.26.252.88']


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    try:
        # Create the folder 'versions' if it doesn't exist
        local("mkdir -p versions")

        # Create the name of the archive with the current date and time
        now = datetime.now()
        file_name = "versions/web_static_{}{}{}{}{}{}.tgz".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second)

        # Compress the contents of the web_static folder into a .tgz archive
        local("tar -cvzf {} web_static".format(file_name))

        return file_name
    except Exception:
        return None


def do_deploy(archive_path):
    '''
    Distributes an archive to the web servers.
    Returns False if the file at the path archive_path doesn’t exist, else it
    deploys it
    '''
    if not os.path.isfile(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Get the base name of the archive file
        archive_filename = archive_path.split('/')[-1]
        archive_name = archive_filename.split('.')[0]

        # Create the folder for the new version on the web server
        run('mkdir -p /data/web_static/releases/{}/'.format(archive_name))

        # Uncompress the archive to the folder on the web server
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(
            archive_filename, archive_name))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

        # Move the contents of the uncompressed folder to the version folder
        my_command = (
            'mv /data/web_static/releases/{}/web_static/*'
            .format(archive_name))
        my_command += ' /data/web_static/releases/{}/'.format(archive_name)
        run(my_command)

        # Remove the empty web_static folder
        run('rm -rf /data/web_static/releases/{}/web_static'
            .format(archive_name))

        # Remove the current symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link to the new version
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(archive_name))
        return True

    except Exception:
        return False


def deploy():
    """
    Calls do_pack and do_deploy functions
    """
    archive_path = do_pack()
    return do_deploy(archive_path)


def do_clean(number=0):
    '''Clean webservers'''
    __local = 'versions/*.tgz'
    __run = '/data/web_static/releases/web_static*'
    if number == 0:
        number = 1
    local("rm -f `ls -t {} | awk 'NR>{}'`".format(__local, number))
    run("rm -rf `ls -td {} | awk 'NR>{}'`".format(__run, number))
