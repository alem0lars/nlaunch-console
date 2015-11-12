class BaseHandler(object):
    """Base handler."""
    def __init__(self, manager):
        super(BaseHandler, self).__init__()
        self.manager = manager
