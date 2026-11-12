class ChefError(Exception):
    '''Base class of all errors raised while parsing or running a Chef recipe.

    Subclasses either pass `msg` (and optionally `lineno`) to this constructor
    or set the attributes (or, in the case of `msg`, a class attribute)
    themselves.

    '''
    msg = None
    lineno = None

    def __init__(self, msg=None, lineno=None):
        Exception.__init__(self, msg)
        self.msg = msg
        self.lineno = lineno

    def __str__(self):
        msg = self.msg
        if msg is None:
            msg = self.__class__.__name__
        if self.lineno is not None:
            msg += ' (line %d)' % self.lineno
        return msg
