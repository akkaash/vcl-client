class VCLResponse(object):
    def __init__(self, status=None):
        self._status = status

    @property
    def status(self):
        return self._status

    def __repr__(self):
        return self.status

class VCLRequestResponse(object):
    def __init__(self, status, request_id):
        self._vcl_response = VCLResponse(status)
        self._request_id = request_id

    @property
    def request_id(self):
        return self._request_id

    @property
    def vcl_response(self):
        return self._vcl_response

    def __repr__(self):
        return str({"status":self.vcl_response, "request_id": self.request_id})

class VCLErrorResponse(object):
    def __init__(self, status, error_code, error_message):
        self._vcl_response = VCLResponse(status)
        self._error_code = error_code
        self._error_message = error_message

    @property
    def error_message(self):
        return self._error_message

    @property
    def vcl_response(self):
        return self._vcl_response



