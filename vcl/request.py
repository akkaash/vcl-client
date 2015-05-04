class VCLRequest(object):

    def __init__(self, request_id=None,
                 image_id=None,
                 image_name=None,
                 start=None,
                 end=None,
                 os=None,
                 is_server=False,
                 state=None,
                 server_name=None):
        self._request_id = request_id
        self._image_id = image_id
        self._image_name = image_name
        self._start = start
        self._end = end
        self._OS = os
        self._is_server = is_server
        self._state = state
        self._server_name = server_name

    @property
    def request_id(self):
        return self._request_id

    @property
    def image_id(self):
        return self._image_id

    @property
    def image_name(self):
        return self._image_name

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def OS(self):
        return self._OS

    @property
    def is_server(self):
        return self._is_server

    @property
    def state(self):
        return self._state

    @property
    def server_name(self):
        return self._server_name

    def __repr__(self):
        return "%s(request_id=%r, image_id=%r, image_name=%r, start=%r, end=%r, OS=%r, is_server=%r, state=%r, server_name=%r)" \
            % (self.__class__, self.request_id, self.image_id, self.image_name,
               self.start, self.end, self.OS, self.is_server,
               self.state, self.server_name)
