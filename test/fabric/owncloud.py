import re
from fabric.api import env, run, hide, task
from envassert import detect, file, port, process, service
from hot.utils.test import get_artifacts, http_check


@task
def check():
    env.platform_family = detect.detect()

    site = 'http://{0}/owncloud'.format(env.host)
    string = 'Files - ownCloud'

    assert file.exists("/var/www/owncloud/config/autoconfig.php"), \
        '/var/www/owncloud/config/autoconfig.php does not exist'

    assert port.is_listening(3306), 'port 3306/mysqld is not listening'
    assert port.is_listening(25), 'port 25/master is not listening'
    assert port.is_listening(443), 'port 443/apache2 is not listening'
    assert port.is_listening(80), 'port 80/apache2 is not listening'

    assert process.is_up("apache2"), 'apache2 process is not running'
    assert process.is_up("mysqld"), 'mysqld process is not running'

    assert service.is_enabled("apache2"), 'service apache2 is not enabled'
    assert service.is_enabled("mysql"), 'service mysql is not enabled'

    assert http_check(site, string), 'owncloud did not respond as expected'


@task
def artifacts():
    env.platform_family = detect.detect()
    get_artifacts()
