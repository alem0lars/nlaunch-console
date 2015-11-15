class BaseHandler(object):
    """Base handler."""
    def __init__(self, dal, manager):
        super(BaseHandler, self).__init__()
        self.dal = dal
        self.manager = manager
