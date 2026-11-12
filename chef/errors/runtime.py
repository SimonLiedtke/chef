from chef.errors import ChefError


class ChefRuntimeError(ChefError):
    pass


class InvalidInputError(ChefRuntimeError):
    def __init__(self, value, lineno=None):
        ChefError.__init__(self, None, lineno)
        self.value = value

    def describe(self):
        return 'invalid input: %r' % self.value

    def repr_args(self):
        return (self.value,)


class UndefinedIngredientError(ChefRuntimeError):
    def __init__(self, ingredient, lineno=None):
        ChefError.__init__(self, None, lineno)
        self.ingredient = ingredient

    def describe(self):
        return 'undefined ingredient: %r' % self.ingredient

    def repr_args(self):
        return (self.ingredient,)


class ContainerIDError(ChefRuntimeError):
    '''Base class of the errors which are related to a mixing bowl or baking
    dish. `type` is either 'mixing bowl' or 'baking dish'.

    '''
    def __init__(self, type, id, lineno=None):
        ChefError.__init__(self, None, lineno)
        self.type = type
        self.id = 1 if id is None else id

    def describe(self):
        raise NotImplementedError(
            'do not raise this exception directly; instead, subclass '
            'this class and define your custom describe method')

    def repr_args(self):
        return (self.type, self.id)


class InvalidContainerIDError(ContainerIDError):
    def describe(self):
        return 'invalid ordinal identifier for %s: %r' % (self.type, self.id)


class NonExistingContainerError(ContainerIDError):
    def describe(self):
        return 'the %s #%d does not exist' % (self.type, self.id)


class EmptyContainerError(ContainerIDError):
    def describe(self):
        return 'the %s #%d is empty' % (self.type, self.id)


class MissingLoopEndError(ChefRuntimeError):
    def __init__(self, verb, lineno=None):
        ChefError.__init__(self, None, lineno)
        self.verb = verb

    def describe(self):
        return (
            'the loop with the verb %r does not have a matching '
            'until-statement to mark the end of the loop' % self.verb)

    def repr_args(self):
        return (self.verb,)
