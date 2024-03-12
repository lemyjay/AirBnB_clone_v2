#!/usr/bin/python3
'''
Deploy files to remote server using Fabric

'''
from fabric.api import env, put, run, local
import os.path
from time import strftime
env.hosts = ['web1.lemyjay.tech', 'web2.lemyjay.tech']


def do_pack():
    '''Generate required files'''
    timenow = strftime('%Y%M%d%H%M%S')
    try:
        local('mkdir -p versions')
        filename = 'versions/web_static_{}.tgz'.format(timenow)
        local('tar -czvf {} web_static/'.format(filename))
        return filename
    except Exception:
        return None


def do_deploy(archive_path):
    '''Upload achive to web servers'''
    if not os.path.isfile(archive_path):
        return False
    try:
        filename = archive_path.split('/')[-1]
        no_ext = filename.split('.')[0]
        path_no_ext = '/data/web_static/releases/{}/'.format(no_ext)
        symlink = '/data/web_static/current'
        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(path_no_ext))
        run('tar -xzf /tmp/{} -C {}'.format(filename, path_no_ext))
        run('rm /tmp/{}'.format(filename))
        run('mv {}web_static/* {}'.format(path_no_ext, path_no_ext))
        run('rm -rf {}web_static'.format(path_no_ext))
        run('rm -rf {}'.format(symlink))
        run('ln -s {} {}'.format(path_no_ext, symlink))
        return True
    except Exception:
        return False


def deploy():
    '''Deploy to the web servers'''
    archive_path = do_pack()
    if archive_path is None:
        return False
    deployment = do_deploy(archive_path)
    return deployment