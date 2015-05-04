class VCLError(Exception):
    def __init__(self, message, error_code):
        super(VCLError, self).__init__(message)
        self.error_code = error_code
