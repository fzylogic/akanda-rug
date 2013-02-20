import httplib2
import json
import netaddr

from akanda.rug.openstack.common import jsonutils

AKANDA_ULA_PREFIX = 'fdca:3ba5:a17a:acda::/64'
AKANDA_MGT_SERVICE_PORT = 5000
AKANDA_BASE_PATH = '/v1/'


def _mgt_url(host, port, path):
    if ':' in host:
        host = '[%s]' % host
    return 'http://%s:%s%s' % (host, port, path)


def is_alive(host, port):
    path = AKANDA_BASE_PATH + 'firewall/labels'
    try:
        h = httplib2.Http(timeout=1.0)
        response, body = h.request(_mgt_url(host, port, path))
        if response.status == 200:
            return True
    except:
        pass
    return False


def get_interfaces(host, port):
    path = AKANDA_BASE_PATH + 'system/interfaces'
    h = httplib2.Http()
    response, body = h.request(_mgt_url(host, port, path))
    return json.loads(body).get('interfaces', [])


def update_config(host, port, config_dict):
    path = AKANDA_BASE_PATH + 'system/config'
    headers = {'Content-type': 'application/json'}

    h = httplib2.Http()
    response, body = h.request(_mgt_url(host, port, path),
                               method='PUT',
                               body=jsonutils.dumps(config_dict),
                               headers=headers)

    if response.status != 200:
        raise Exception('Config update failed: %s' % body)
    else:
        return json.loads(body)


def read_labels(host, port):
    path = AKANDA_BASE_PATH + 'firewall/labels'
    h = httplib2.Http()
    response, body = h.request(_mgt_url(host, port, path), method='POST')
    return json.loads(body).get('labels', [])