import requests
import json
import os


class ProxyAPI(object):
    def __init__(self, **kwargs):
        pass

    def proxy_changed(self, **kwargs):
        pass

    def get_service_url(self, **kwargs):
        pass


class NoProxy(ProxyAPI):
    def __init__(self, **kwargs):
        self.proxy_host = None
        self.proxy_port = 0

    def proxy_changed(self, **kwargs):
        return False

    def get_service_url(self, **kwargs):
        return self.proxy_host, self.proxy_port


class Serveo(ProxyAPI):
    def __init__(self,
                 host=os.environ.get('SERVEO_HOST'),
                 port=os.environ.get('SERVEO_PORT'),
                 **kwargs):
        self.proxy_host = host
        self.proxy_port = int(port)

    def proxy_changed(self, **kwargs):
        return False

    def get_service_url(self, **kwargs):
        return self.proxy_host, self.proxy_port


class RemoteIt(ProxyAPI):
    def __init__(self,
                 dev_key=os.environ.get('REMOTEIT_DEVELOPER_KEY'),
                 username=os.environ.get('REMOTEIT_USERNAME'),
                 password=os.environ.get('REMOTEIT_PASSWORD')):
        self.http_sess = requests.Session()
        self.http_sess.mount('https://', requests.adapters.HTTPAdapter(max_retries=5))
        self.dev_key = dev_key
        self.username = username
        self.password = password

        self.proxy_host = None
        self.proxy_port = None
        self.__login()

    def __login(self):
        url = 'https://api.remot3.it/apv/v27/user/login'
        headers = {'developerkey': self.dev_key}
        body = {'password': self.password, 'username': self.username}
        response = self.http_sess.post(url, data=json.dumps(body), headers=headers)
        response_body = response.json()
        self.token = response_body['token']

    def get_service_url(self, service_id=os.environ.get('REMOTEIT_SERVICE_ID'), **kwargs):
        headers = {'developerkey': self.dev_key,
                   'token': self.token}
        body = {'deviceaddress': service_id, 'wait': True, 'hostip': '0.0.0.0'}

        url = 'https://api.remot3.it/apv/v27/device/connect'
        response = self.http_sess.post(url, data=json.dumps(body), headers=headers)
        response_body = response.json()
        self.proxy_host = response_body['connection']['proxyserver']
        self.proxy_port = int(response_body['connection']['proxyport'])
        return self.proxy_host, self.proxy_port

    def proxy_changed(self, service_id=os.environ.get('REMOTEIT_SERVICE_ID'), **kwargs):
        prev_host, prev_port = self.proxy_host, self.proxy_port
        changed = self.get_service_url(service_id=service_id) != (prev_host, prev_port)
        if changed:
            print('Got new Remote.iT proxy: {}:{}'.format(self.proxy_host, self.proxy_port))
        return changed


if __name__ == '__main__':
    print(RemoteIt().get_service_url())
