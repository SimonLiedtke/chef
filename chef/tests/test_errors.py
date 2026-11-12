import pytest

from chef.errors import ChefError
from chef.errors.runtime import ChefRuntimeError, InvalidInputError,\
        UndefinedIngredientError, ContainerIDError, InvalidContainerIDError,\
        NonExistingContainerError, EmptyContainerError, MissingLoopEndError
from chef.errors import syntax as syntax_errors


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


class TestCustomSyntaxErrors(object):
    def test_messages(self):
        for cls, msg in [
                (syntax_errors.MissingTitleError, 'missing title'),
                (syntax_errors.MissingTrailingFullStopError,
                 'missing trailing full stop'),
                (syntax_errors.MissingEmptyLineError, 'missing empty line'),
                (syntax_errors.InvalidCookingTimeError, 'invalid cooking time'),
                (syntax_errors.InvalidOvenTemperature,
                 'invalid oven temperature')]:
            name = cls.__name__
            check(cls(), msg, '%s()' % name)
            check(cls(3), msg + ' (line 3)', '%s(3)' % name)
            assert cls(3).msg == msg
            assert cls(3).lineno == 3


class TestSyntaxErrors(object):
    def test_generic_syntax_error(self):
        check(syntax_errors.ChefSyntaxError('invalid method name', 5),
              'invalid method name (line 5)',
              "ChefSyntaxError('invalid method name', 5)")

    def test_invalid_measure_type_value(self):
        message = (
            'invalid measure type value (\'big\'); only the values "heaped" '
            'and "level" are allowed')
        check(syntax_errors.InvalidMeasureTypeValue('big'),
              message, "InvalidMeasureTypeValue('big')")
        check(syntax_errors.InvalidMeasureTypeValue('big', 2),
              message + ' (line 2)', "InvalidMeasureTypeValue('big', 2)")

    def test_non_matching_measure_type(self):
        message = (
            "the measure 'g' and the measure type 'heaped' "
            "do not form a valid measure declaration")
        check(syntax_errors.NonMatchingMeasureTypeError('g', 'heaped'),
              message, "NonMatchingMeasureTypeError('g', 'heaped')")
        check(syntax_errors.NonMatchingMeasureTypeError('g', 'heaped', 4),
              message + ' (line 4)',
              "NonMatchingMeasureTypeError('g', 'heaped', 4)")

    def test_not_allowed_time(self):
        message = 'the time 0 is too low; only positive values are allowed'
        check(syntax_errors.NotAllowedTimeError(0),
              message, 'NotAllowedTimeError(0)')
        check(syntax_errors.NotAllowedTimeError(0, 6),
              message + ' (line 6)', 'NotAllowedTimeError(0, 6)')

    def test_ordinal_identifier(self):
        check(syntax_errors.OrdinalIdentifierError('0th'),
              "not a valid ordinal identifier: '0th'",
              "OrdinalIdentifierError('0th')")
        check(syntax_errors.OrdinalIdentifierError('0th', 3),
              "not a valid ordinal identifier: '0th' (line 3)",
              "OrdinalIdentifierError('0th', 3)")

    def test_non_matching_suffix(self):
        message = (
            "the number 1 and the suffix 'th' do not form a valid "
            "ordinal identifier")
        check(syntax_errors.NonMatchingSuffixError(1, 'th'),
              message, "NonMatchingSuffixError(1, 'th')")
        check(syntax_errors.NonMatchingSuffixError(1, 'th', 8),
              message + ' (line 8)', "NonMatchingSuffixError(1, 'th', 8)")

    def test_non_matching_suffix_is_an_ordinal_identifier_error(self):
        error = syntax_errors.NonMatchingSuffixError(1, 'th')
        assert isinstance(error, syntax_errors.OrdinalIdentifierError)
        assert (error.number, error.suffix) == (1, 'th')

    def test_non_matching_unit(self):
        message = (
            "the number 2 and the unit 'hour' do not form a valid "
            "cooking time")
        check(syntax_errors.NonMatchingUnitError(2, 'hour'),
              message, "NonMatchingUnitError(2, 'hour')")
        check(syntax_errors.NonMatchingUnitError(2, 'hour', 5),
              message + ' (line 5)', "NonMatchingUnitError(2, 'hour', 5)")

    def test_invalid_time_declaration(self):
        message = "invalid time declaration: '1 hours'"
        check(syntax_errors.InvalidTimeDeclarationError(1, 'hours'),
              message, "InvalidTimeDeclarationError(1, 'hours')")
        error = syntax_errors.InvalidTimeDeclarationError(1, 'hours', 9)
        check(error, message + ' (line 9)',
              "InvalidTimeDeclarationError(1, 'hours', 9)")
        assert error.lineno == 9

    def test_invalid_command(self):
        check(syntax_errors.InvalidCommandError('Put'),
              "invalid command 'Put'", "InvalidCommandError('Put')")
        check(syntax_errors.InvalidCommandError('Put', 7),
              "invalid command 'Put' (line 7)",
              "InvalidCommandError('Put', 7)")
