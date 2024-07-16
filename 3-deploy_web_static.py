#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
import os.path
from datetime import datetime
from fabric.api import env, local, put, run

env.hosts = ['54.162.232.135', '18.234.249.5']

def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                         dt.month,
                                                         dt.day,
                                                         dt.hour,
                                                         dt.minute,
                                                         dt.second)
    if not os.path.isdir("versions"):
        if local("mkdir -p versions").failed:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed:
        return None
    return file

def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if not os.path.isfile(archive_path):
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    print("Uploading archive to /tmp/{}".format(file))
    if put(archive_path, "/tmp/{}".format(file)).failed:
        return False

    print("Creating release directory")
    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed:
        return False

    print("Extracting archive")
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name)).failed:
        return False

    print("Removing archive from /tmp")
    if run("rm /tmp/{}".format(file)).failed:
        return False

    print("Moving contents to the release directory")
    if run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name)).failed:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".format(name)).failed:
        return False

    print("Updating the symbolic link")
    if run("rm -rf /data/web_static/current").failed:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)).failed:
        return False

    print("New version deployed!")
    return True

def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)

