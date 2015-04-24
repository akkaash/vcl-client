import getpass
from vcl_serverproxy import VCLServerProxy
import xmlrpclib


class VCL(object):
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.verbose = 0
        self.client = VCLServerProxy(self.url, self.username, self.password, verbose=0)

    def test(self, test_string):
        # client = VCLServerProxy(self.url, self.username, self.password, verbose=0)
        rc = self.client.XMLRPCtest(test_string)
        return rc

    def get_images(self):
        client = VCLServerProxy(self.url, self.username, self.password, verbose=0)
        rc = self.client.XMLRPCgetImages()
        return rc

    def add_request(self, image_id, start, length, count):
        requests = range(count)
        for i in requests:
            rc = self.client.XMLRPCaddRequest(image_id, start, length)
            yield rc

    def end_request(self, request_id):
        return self.client.XMLRPCendRequest(request_id)

    def get_requestIds(self):
        return self.client.XMLRPCgetRequestIds()

    def get_request_status(self, request_id):
        return self.client.XMLRPCgetRequestStatus(request_id)

    def get_request_connect_data(self, request_id, remote_ip):
        return self.client.XMLRPCgetRequestConnectData(request_id, remote_ip)


class VCLServerProxy(xmlrpclib.ServerProxy):
    __userid = ''
    __passwd = ''

    def __init__(self, uri, userid, passwd, transport=None, encoding=None,
                 verbose=0, allow_none=0, use_datetime=0):
        self.__userid = userid
        self.__passwd = passwd
        # establish a "logical" server connection

        # get the url
        type, uri = urllib.splittype(uri)
        if type not in ("http", "https"):
            raise IOError, "unsupported XML-RPC protocol"
        self.__host, self.__handler = urllib.splithost(uri)
        if not self.__handler:
            self.__handler = "/RPC2"
        if transport is None:
            transport = VCLTransport()
        self.__transport = transport
        self.__encoding = encoding
        self.__verbose = verbose
        self.__allow_none = allow_none

    def __request(self, method_name, params):
        request = xmlrpclib.dumps(params, method_name, encoding=self.__encoding,
                                  allow_none=self.__allow_none)
        response = self.__transport.request(
            self.__host,
            self.__userid,
            self.__passwd,
            self.__handler,
            request,
            verbose=self.__verbose
        )
        if len(response) == 1:
            response = response[0]
        return response

    def __getattr__(self, name):
        return xmlrpclib._Method(self.__request, name)


class VCLTransport(xmlrpclib.SafeTransport):
    ##
    # Send a complete request, and parse the response.
    #
    # @param host Target host.
    # @param handler Target PRC handler.
    # @param request_body XML-RPC request body.
    # @param verbose Debugging flag.
    # @return Parsed response.

    def request(self, host, userid, passwd, handler, request_body, verbose=0):
        # issue XML-RPC request

        h = self.make_connection(host)
        if verbose:
            h.set_debuglevel(1)
        self.send_request(h, handler, request_body)
        h.putheader('X-APIVERSION', '2')
        h.putheader('X-User', userid)
        h.putheader('X-Pass', passwd)
        self.send_host(h, host)
        self.send_user_agent(h)
        self.send_content(h, request_body)
        response = h.getresponse()
        errcode, errmsg, headers = response.status, response.msg, response.getheaders()
        if errcode != 200:
            raise xmlrpclib.ProtocolError(
                host + handler,
                errcode, errmsg,
                headers
            )
        self.verbose = verbose
        resp = response.read()
        try:
            resp = xmlrpclib.loads(resp)[0]
        except xmlrpclib.Fault, err:
            if err.faultCode == 3:
                print "ERROR: Received '%s' error. " \
                      "The credentials you supplied to log in to the VCL site were not accepted." % err.faultString
            elif err.faultCode == 4:
                print "ERROR: %s" % err.faultString
            elif err.faultCode == 5:
                print "ERROR: Received '%s' error. " \
                      "The VCL site could not establish a connection with your authentication server." % err.faultString
            elif err.faultCode == 6:
                print "ERROR: Received '%s' error. " \
                      "The VCL site could not determine a method to use to authenticate the supplied user." \
                      % err.faultString
            else:
                print "ERROR: Received '%s' error from VCL site." % err.faultString

        return resp
