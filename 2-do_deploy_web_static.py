#!/usr/bin/python3
"""
A Fabric script that distributes the archive to the web
servers using do_deploy function.
"""

from fabric.api import env, put, run
from os.path import exists

# Define the user and SSH key for accessing the server
env.user = 'ubuntu'
env.key_filename = '~/.ssh/my_key'

# Define the list of web servers
env.hosts = ['100.25.0.107', '100.26.252.88']


def do_deploy(archive_path):
    '''
    Distributes an archive to the web servers.
    Returns False if the file at the path archive_path doesn’t exist, else it
    deploys it
    '''
    if not exists(archive_path):
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

        print("New version deployed!")
        return True

    except Exception as e:
        return False
