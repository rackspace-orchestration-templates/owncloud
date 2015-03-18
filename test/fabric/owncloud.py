import re
from fabric.api import env, run, hide, task
from envassert import detect, file, port, process, service
from hot.utils.test import get_artifacts


def owncloud_is_responding():
    with hide('running', 'stdout'):
        wget_cmd = 'wget --quiet --output-document - http://localhost/'
        page = run(wget_cmd)
        if re.search('web services under your control', page):
            return True
        else:
            print "oops, didn't find desired text in page."
            print "page contents was: {}".format(page)
            return False


@task
def check():
    env.platform_family = detect.detect()

    assert file.exists("/etc/apache2/sites-enabled/owncloud.conf"), \
        '/etc/apache2/sites-enabled/owncloud.conf does not exist'

    assert port.is_listening(3306), 'port 3306/mysqld is not listening'
    assert port.is_listening(25), 'port 25/master is not listening'
    assert port.is_listening(443), 'port 443/apache2 is not listening'
    assert port.is_listening(80), 'port 80/apache2 is not listening'

    assert process.is_up("apache2"), 'apache2 process is not running'
    assert process.is_up("mysqld"), 'mysqld process is not running'

    assert service.is_enabled("apache2"), 'service apache2 is not enabled'
    assert service.is_enabled("mysql"), 'service mysql is not enabled'

    assert owncloud_is_responding(), 'owncloud did not respond as expected'


@task
def artifacts():
    env.platform_family = detect.detect()
    get_artifacts()
