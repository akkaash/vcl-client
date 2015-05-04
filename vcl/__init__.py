import xmlrpclib
import urllib
import logging
import logging.config

import errors
import response
import request


LOG = logging.getLogger(__name__)
LOG.setLevel(level=logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
LOG.addHandler(ch)


class VCL(object):

    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.verbose = 0
        self.client = VCLServerProxy(
            self.url, self.username, self.password, verbose=0)

    def test(self, test_string):
        # client = VCLServerProxy(self.url, self.username, self.password, verbose=0)
        rc = self.client.XMLRPCtest(test_string)
        return rc

    def get_images(self):
        client = VCLServerProxy(
            self.url, self.username, self.password, verbose=0)
        rc = self.client.XMLRPCgetImages()
        return rc

    def add_request(self, image_id=None, start="now", length=60, count=1):
        if image_id is None or not isinstance(image_id, int):
            raise ValueError("image_id expected to be integer")
        if start != "now" and not isinstance(start, int):
            raise ValueError(
                "start time should be 'now' or integer UNIX timestamp")
        if length < 0:
            raise ValueError("reservation length cannot be negative")
        if count <= 0:
            return
        responses = []
        for i in range(count):
            try:
                rc = self.client.XMLRPCaddRequest(image_id, start, length)
                LOG.debug(msg=rc)
                if rc['status'] == "success":
                    responses.append(response.VCLRequestResponse(
                        status=rc['status'],
                        request_id=rc['requestid']))
                elif rc['status'] == "error":
                    raise errors.VCLError(message=rc['errormsg'],
                                          error_code=rc['errorcode'])
            except errors.VCLError, e:
                LOG.error(
                    "Error Code: {1} Message: {0} ".format(e, e.error_code))
                responses.append(response.VCLErrorResponse(status="error",
                                                           error_code=e.error_code,
                                                           error_message=e.message))
        return responses

    def end_request(self, request_id):
        ret = None
        if request_id < 0:
            raise ValueError("request id should be positive")
        try:
            rc = self.client.XMLRPCendRequest(request_id)
            if rc['status'] == "success":
                ret = response.VCLResponse(rc['status'])
            else:
                raise errors.VCLError(message=rc['errormsg'],
                                      error_code=rc['errorcode'])
        except errors.VCLError, e:
            LOG.error(
                msg="Error Code: {1} Message: {0}".format(e, e.error_code))
            ret = response.VCLErrorResponse(status="error",
                                            error_code=e.error_code,
                                            error_message=e.message)
        finally:
            return ret

    def get_request_ids(self):
        res = []
        try:
            rc = self.client.XMLRPCgetRequestIds()
            LOG.debug(msg=rc)
            if rc['status'] == "success":
                LOG.debug(msg="success")
                for req in rc['requests']:
                    LOG.debug(msg="request: {}".format(req))
                    res.append(request.VCLRequest(
                        request_id=req['requestid'],
                        image_id=req['imageid'],
                        image_name=req['imagename'],
                        start=req['start'],
                        end=req['end'],
                        os=req['OS'],
                        is_server=True if req['isserver'] == 1 else False,
                        state=req['state'],
                        server_name=req['servername'] if req['isserver'] else None))
        except errors.VCLError, e:
            LOG.error(
                msg="Error Code: {1} Message: {0}".format(e, e.error_code))
            res = response.VCLErrorResponse(status="error",
                                            error_code=e.error_code,
                                            error_message=e.message)
        except Exception, e:
            raise e
        finally:
            return res

    def get_request_status(self, request_id):
        res = None
        try:
            rc = self.client.XMLRPCgetRequestStatus(request_id)
            if rc['status'] == "loading":
                res = response.VCLResponse(status=rc['status'],
                                           time=rc['time'])
            elif rc['status'] == "error":
                raise errors.VCLError(message=rc['errormsg'],
                                      error_code=rc['errorcode'])
            else:
                res = response.VCLResponse(status=rc['status'])
        except errors.VCLError, e:
            LOG.error(msg="{0} {1}".format(request_id, e.message))
            res = response.VCLErrorResponse(status="error",
                                            error_code=e.faultCode,
                                            error_message=e.message)
        finally:
            return res

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
        protocol_type, uri = urllib.splittype(uri)
        if protocol_type not in ("http", "https"):
            LOG.error(msg="input URL: {0}".format(uri))
            LOG.error(
                msg="{0}: unsupported XML-RPC protocol".format(protocol_type))
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
            # if err.faultCode == 3:
            #     raise errors.VCLError(
            #         err.faultString, err.faultCode)
            # elif err.faultCode == 4:
            #     LOG.error("%s" % err.faultString)
            # elif err.faultCode == 5:
            #     LOG.error("Received '%s' error. "
            #               "The VCL site could not establish a connection with your authentication server." % err.faultString)
            # elif err.faultCode == 6:
            #     LOG.error("Received '%s' error. "
            #               "The VCL site could not determine a method to use to authenticate the supplied user."
            #               % err.faultString)
            # else:
            #     LOG.error("ERROR: Received '%s' error from VCL site." %
            #               err.faultString)

            raise errors.VCLError(message=err.faultString,
                                  error_code=err.faultCode)

        return resp
