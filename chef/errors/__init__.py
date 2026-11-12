class ChefError(Exception):
    '''Base class of all errors raised while parsing or running a Chef recipe.

    Subclasses either pass `msg` (and optionally `lineno`) to this constructor
    or set the attributes (or, in the case of `msg`, a class attribute)
    themselves.

    To customise the text of an error, override `describe`; the line number is
    appended by `__str__`. To customise `repr()`, override `repr_args`.

    '''
    msg = None
    lineno = None

    def __init__(self, msg=None, lineno=None):
        Exception.__init__(self, msg)
        self.msg = msg
        self.lineno = lineno

    def describe(self):
        'Return the text of the error, without the line number.'
        if self.msg is None:
            return self.__class__.__name__
        return self.msg

    def repr_args(self):
        'Return the positional constructor arguments, without the line number.'
        if self.msg is None and self.lineno is None:
            return ()
        return (self.msg,)

    def __str__(self):
        text = self.describe()
        if self.lineno is not None:
            text += ' (line %d)' % self.lineno
        return text

    def __repr__(self):
        args = self.repr_args()
        if self.lineno is not None:
            args = args + (self.lineno,)
        return '%s(%s)' % (
            self.__class__.__name__, ', '.join([repr(a) for a in args]))
