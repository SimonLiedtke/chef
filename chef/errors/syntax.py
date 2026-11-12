from chef.errors import ChefError


class ChefSyntaxError(ChefError):
    pass


class CustomSyntaxError(ChefSyntaxError):
    '''Base class of syntax errors without any arguments besides the line
    number. Subclasses set the message in the class attribute `msg`.

    '''
    def __init__(self, lineno=None):
        ChefError.__init__(self, self.msg, lineno)

    def repr_args(self):
        return ()


class MissingTitleError(CustomSyntaxError):
    msg = 'missing title'


class MissingTrailingFullStopError(CustomSyntaxError):
    msg = 'missing trailing full stop'


class MissingEmptyLineError(CustomSyntaxError):
    msg = 'missing empty line'


class InvalidCookingTimeError(CustomSyntaxError):
    msg = 'invalid cooking time'


class InvalidOvenTemperature(CustomSyntaxError):
    msg = 'invalid oven temperature'


class InvalidMeasureTypeValue(CustomSyntaxError):
    def __init__(self, measure_type, lineno=None):
        ChefError.__init__(self, None, lineno)
        self.measure_type = measure_type

    def describe(self):
        return (
            'invalid measure type value (%r); only the values "heaped" and '
            '"level" are allowed' % self.measure_type)

    def repr_args(self):
        return (self.measure_type,)


class NonMatchingMeasureTypeError(CustomSyntaxError):
    def __init__(self, measure, measure_type, lineno=None):
        ChefError.__init__(self, None, lineno)
        self.measure = measure
        self.measure_type = measure_type

    def describe(self):
        return (
            'the measure %r and the measure type %r '
            'do not form a valid measure declaration' % (
                self.measure, self.measure_type))

    def repr_args(self):
        return (self.measure, self.measure_type)


class NotAllowedTimeError(ChefSyntaxError):
    def __init__(self, time, lineno=None):
        ChefError.__init__(self, None, lineno)
        self.time = time

    def describe(self):
        return (
            'the time %d is too low; '
            'only positive values are allowed' % self.time)

    def repr_args(self):
        return (self.time,)


class OrdinalIdentifierError(ChefSyntaxError):
    def __init__(self, ordinal_identifier, lineno=None):
        ChefError.__init__(self, None, lineno)
        self.ordinal_identifier = ordinal_identifier

    def describe(self):
        return 'not a valid ordinal identifier: %r' % self.ordinal_identifier

    def repr_args(self):
        return (self.ordinal_identifier,)


class NonMatchingSuffixError(OrdinalIdentifierError):
    def __init__(self, number, suffix, lineno=None):
        ChefError.__init__(self, None, lineno)
        self.number = number
        self.suffix = suffix

    def describe(self):
        return (
            'the number %d and the suffix %r do not form a valid '
            'ordinal identifier' % (self.number, self.suffix))

    def repr_args(self):
        return (self.number, self.suffix)


class NonMatchingUnitError(ChefSyntaxError):
    def __init__(self, number, unit, lineno=None):
        ChefError.__init__(self, None, lineno)
        self.number = number
        self.unit = unit

    def describe(self):
        return (
            'the number %d and the unit %r do not form a valid '
            'cooking time' % (self.number, self.unit))

    def repr_args(self):
        return (self.number, self.unit)


class InvalidTimeDeclarationError(ChefSyntaxError):
    def __init__(self, hours, format, lineno=None):
        ChefError.__init__(self, None, lineno)
        self.hours = hours
        self.format = format

    def describe(self):
        return "invalid time declaration: '%d %s'" % (self.hours, self.format)

    def repr_args(self):
        return (self.hours, self.format)


class InvalidCommandError(ChefSyntaxError):
    def __init__(self, command, lineno=None):
        ChefError.__init__(self, None, lineno)
        self.cmd = command

    def describe(self):
        return 'invalid command %r' % self.cmd

    def repr_args(self):
        return (self.cmd,)
