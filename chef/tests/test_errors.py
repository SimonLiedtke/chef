from chef.errors import ChefError


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
