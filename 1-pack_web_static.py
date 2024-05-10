#!/usr/bin/python3
"""  a Fabric script that generates a .tgz archive from the
content of the web_static"""
from fabric.api import *
from datetime import datetime


def do_pack():
    """ using the do pack generate a .tgz """
    local("mkdir -p versions")
    now = datetime.utcnow()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    archive_name = "versions/web_static_{}.tgz".format(timestamp)
    result = local("tar -cvzf {} web_static".format(archive_name))

    if result.succeeded:
        return archive_name
    else:
        return None
