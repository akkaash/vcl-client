import getpass
from vcl_serverproxy import VCLServerProxy


class VCLApi(object):
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.verbose = 0

    def test(self, test_string):
        client = VCLServerProxy(self.url, self.username, self.password, verbose=0)
        rc = client.XMLRPCtest(test_string)
        return rc

    def get_images(self):
        client = VCLServerProxy(self.url, self.username, self.password, verbose=0)
        rc = client.XMLRPCgetImages()
        return rc

    def add_request(self, image_id, start, length):
        client = VCLServerProxy(self.url, self.username, self.password, verbose=0)
        rc = client.XMLRPCaddRequest(image_id, start, length)
        return rc
