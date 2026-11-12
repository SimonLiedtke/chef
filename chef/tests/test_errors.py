import pytest

from chef.errors import ChefError
from chef.errors.runtime import ChefRuntimeError, InvalidInputError,\
        UndefinedIngredientError, ContainerIDError, InvalidContainerIDError,\
        NonExistingContainerError, EmptyContainerError, MissingLoopEndError


def check(error, expected_str, expected_repr):
    assert str(error) == expected_str
    assert repr(error) == expected_repr


class TestChefError(object):
    def test_without_arguments(self):
        check(ChefError(), 'ChefError', 'ChefError()')

    def test_message(self):
        check(ChefError('oops'), 'oops', "ChefError('oops')")

    def test_message_and_lineno(self):
        error = ChefError('oops', 12)
        check(error, 'oops (line 12)', "ChefError('oops', 12)")
        assert error.msg == 'oops'
        assert error.lineno == 12

    def test_lineno_only(self):
        check(ChefError(lineno=3), 'ChefError (line 3)', 'ChefError(None, 3)')


class TestRuntimeErrors(object):
    def test_invalid_input(self):
        check(InvalidInputError('abc'),
              "invalid input: 'abc'", "InvalidInputError('abc')")
        check(InvalidInputError('abc', 4),
              "invalid input: 'abc' (line 4)", "InvalidInputError('abc', 4)")

    def test_undefined_ingredient(self):
        check(UndefinedIngredientError('milk'),
              "undefined ingredient: 'milk'",
              "UndefinedIngredientError('milk')")
        check(UndefinedIngredientError('milk', 9),
              "undefined ingredient: 'milk' (line 9)",
              "UndefinedIngredientError('milk', 9)")

    def test_invalid_container_id(self):
        check(InvalidContainerIDError('mixing bowl', 0),
              "invalid ordinal identifier for mixing bowl: 0",
              "InvalidContainerIDError('mixing bowl', 0)")
        check(InvalidContainerIDError('baking dish', -1, 5),
              "invalid ordinal identifier for baking dish: -1 (line 5)",
              "InvalidContainerIDError('baking dish', -1, 5)")

    def test_non_existing_container(self):
        check(NonExistingContainerError('mixing bowl', 3),
              'the mixing bowl #3 does not exist',
              "NonExistingContainerError('mixing bowl', 3)")
        check(NonExistingContainerError('baking dish', 2, 8),
              'the baking dish #2 does not exist (line 8)',
              "NonExistingContainerError('baking dish', 2, 8)")

    def test_empty_container(self):
        check(EmptyContainerError('mixing bowl', 2),
              'the mixing bowl #2 is empty',
              "EmptyContainerError('mixing bowl', 2)")
        check(EmptyContainerError('baking dish', 1, 6),
              'the baking dish #1 is empty (line 6)',
              "EmptyContainerError('baking dish', 1, 6)")

    def test_container_id_defaults_to_one(self):
        error = EmptyContainerError('mixing bowl', None)
        assert error.id == 1
        assert str(error) == 'the mixing bowl #1 is empty'

    def test_container_id_error_must_be_subclassed(self):
        with pytest.raises(NotImplementedError):
            str(ContainerIDError('mixing bowl', 1))

    def test_missing_loop_end(self):
        message = (
            "the loop with the verb 'Count' does not have a matching "
            "until-statement to mark the end of the loop")
        check(MissingLoopEndError('Count'),
              message, "MissingLoopEndError('Count')")
        check(MissingLoopEndError('Count', 7),
              message + ' (line 7)', "MissingLoopEndError('Count', 7)")

    def test_are_chef_errors(self):
        assert isinstance(InvalidInputError('x'), ChefRuntimeError)
        assert isinstance(ChefRuntimeError(), ChefError)
