class NcmsError(Exception):
    def __init__(self, message, error=None):
        super(NcmsError, self).__init__(message)
        self.error = error
        self.message = message


class NcmsWebError(NcmsError):
    def __init__(self, message, path, error=None):
        super(NcmsWebError, self).__init__(message, error)
        self.error = error
        self.message = message
        self.path = path


class NcmsWebApiError(NcmsWebError):
    def __init__(self, message, path, error=None):
        super(NcmsWebApiError, self).__init__(message, path, error)
        self.error = error
        self.message = message
        self.path = path


class NcmsWebApiError(NcmsWebError):
    def __init__(self, message, path, error=None):
        super(NcmsWebApiError, self).__init__(message, path, error)
        self.error = error
        self.message = message
        self.path = path


class NcmsWebApiValueError(NcmsWebApiError):
    def __init__(self, value, message, path, error=None):
        super(NcmsWebApiError, self).__init__(message, path, error)
        self.error = error
        self.message = message
        self.path = path
        self.value = value
