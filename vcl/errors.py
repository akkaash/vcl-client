class VCLError(Exception):
    def __init__(self, message, error_code):
        super(VCLError, self).__init__(message)
        self._error_code = error_code

    @property
    def error_code(self):
        return self._error_code

    def __repr__(self):
        return "%s(error_code=%r, message=%r)" % (self.__class__, self.error_code,
                                                  self.message)
