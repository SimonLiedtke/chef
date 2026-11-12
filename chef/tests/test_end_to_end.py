# coding: utf-8
'''Run the command line interface (`bin/chef`) in a separate process.'''
from __future__ import with_statement

import os
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
CHEF = os.path.join(ROOT, 'bin', 'chef')
EXAMPLE_DIR = os.path.join(ROOT, 'examples')


def run_chef(args, stdin_data='', recipe=None):
    '''Run `bin/chef` with the arguments `args` and the data `stdin_data` on
    its standard input. If `recipe` is given, it is written to a temporary file
    which is passed with `-f`. Return a tuple (return code, stdout, stderr).

    '''
    args = list(args)
    path = None
    if recipe is not None:
        fd, path = tempfile.mkstemp(suffix='.chef')
        try:
            os.write(fd, recipe.encode('utf-8'))
        finally:
            os.close(fd)
        args += ['-f', path]
    env = dict(os.environ)
    env['PYTHONPATH'] = os.pathsep.join(
        [ROOT] + [p for p in [env.get('PYTHONPATH')] if p])
    try:
        process = subprocess.Popen(
            [sys.executable, CHEF] + args, env=env, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate(stdin_data.encode('utf-8'))
    finally:
        if path is not None:
            os.remove(path)
    return process.returncode, out.decode('utf-8'), err.decode('utf-8')


def example_path(name):
    return os.path.join(EXAMPLE_DIR, name + '.chef')


def multiplication_table():
    return ''.join(
        ''.join([' %d' % (i * j) for j in range(1, 11)]) + '\n'
        for i in range(1, 11))


def recipe(ingredients, method, serves='Serves 1.'):
    'Build a small recipe from the lines of the ingredient list and method.'
    return 'A test.\n\nIngredients.\n%s\n\nMethod.\n%s\n\n%s\n' % (
        '\n'.join(ingredients), '\n'.join(method), serves)


class TestExamples(object):
    params = {
        'test_example': [
            {'name': 'helloworld', 'expected': 'Hello world!\n'},
            {'name': 'loop', 'expected': '012345678910'},
            {'name': 'simple_nested_loop', 'expected': '123\n123\n123\n'},
            {'name': 'nested_loop', 'expected': multiplication_table()}],
        'test_example_via_stdin': [
            {'name': 'helloworld', 'expected': 'Hello world!\n'},
            {'name': 'loop', 'expected': '012345678910'}]}

    def test_example(self, name, expected):
        returncode, out, err = run_chef(['-f', example_path(name)])
        assert (returncode, out, err) == (0, expected, '')

    def test_example_via_stdin(self, name, expected):
        with open(example_path(name)) as f:
            source = f.read()
        returncode, out, err = run_chef([], source)
        assert (returncode, out, err) == (0, expected, '')


class TestCommands(object):
    params = {
        'test_calculation': [
            {'command': 'Add', 'expected': '9'},
            {'command': 'Remove', 'expected': '3'},
            {'command': 'Combine', 'expected': '18'},
            {'command': 'Divide', 'expected': '2'}]}

    def test_calculation(self, command, expected):
        source = recipe(
            ['6 a', '3 b'],
            ['Put a into mixing bowl.',
             '%s b.' % command,
             'Pour contents of the mixing bowl into the baking dish.'])
        assert run_chef([], recipe=source) == (0, expected, '')

    def test_take(self):
        source = recipe(
            ['0 n'],
            ['Take n from refrigerator.',
             'Put n into mixing bowl.',
             'Liquefy contents of the mixing bowl.',
             'Pour contents of the mixing bowl into the baking dish.'])
        assert run_chef([], '65\n', source) == (0, 'A', '')

    def test_fold(self):
        source = recipe(
            ['4 a', '0 b'],
            ['Put a into mixing bowl.',
             'Fold b into mixing bowl.',
             'Put b into mixing bowl.',
             'Put b into mixing bowl.',
             'Pour contents of the mixing bowl into the baking dish.'])
        assert run_chef([], recipe=source) == (0, '44', '')

    def test_stir(self):
        source = recipe(
            ['1 a', '2 b', '3 c'],
            ['Put a into mixing bowl.',
             'Put b into mixing bowl.',
             'Put c into mixing bowl.',
             'Stir the mixing bowl for 1 minutes.',
             'Pour contents of the mixing bowl into the baking dish.'])
        # the baking dish is served from the top
        assert run_chef([], recipe=source) == (0, '231', '')

    def test_add_dry_ingredients(self):
        source = recipe(
            ['5 g flour', '7 g sugar', '3 ml milk'],
            ['Add dry ingredients.',
             'Pour contents of the mixing bowl into the baking dish.'])
        assert run_chef([], recipe=source) == (0, '12', '')

    def test_refrigerate_ends_the_recipe(self):
        source = recipe(
            ['5 a'],
            ['Put a into mixing bowl.',
             'Pour contents of the mixing bowl into the baking dish.',
             'Refrigerate for 1 hour.',
             'Put a into mixing bowl.',
             'Pour contents of the mixing bowl into the baking dish.'])
        assert run_chef([], recipe=source) == (0, '5', '')

    def test_without_serves_nothing_is_printed(self):
        source = recipe(
            ['5 a'],
            ['Put a into mixing bowl.',
             'Pour contents of the mixing bowl into the baking dish.'],
            serves='')
        assert run_chef([], recipe=source) == (0, '', '')


class TestErrors(object):
    def test_invalid_command(self):
        source = recipe(['1 a'], ['Put a into the mixing bowl.'])
        returncode, out, err = run_chef([], recipe=source)
        assert returncode != 0
        assert "invalid command 'Put'" in out

    def test_unknown_method(self):
        source = recipe(['1 a'], ['Frobnicate.'])
        returncode, out, err = run_chef([], recipe=source)
        assert returncode != 0
        assert 'invalid method name' in out

    def test_loop_without_end(self):
        source = recipe(['1 a'], ['Frobnicate the a.'])
        returncode, out, err = run_chef([], recipe=source)
        assert returncode != 0
        assert 'does not have a matching until-statement' in out

    def test_runtime_error(self):
        source = recipe(['1 a'], ['Put b into mixing bowl.'])
        returncode, out, err = run_chef([], recipe=source)
        assert returncode != 0
        assert "undefined ingredient: 'b'" in out

    def test_invalid_input(self):
        source = recipe(['0 n'], ['Take n from refrigerator.'])
        returncode, out, err = run_chef([], 'not a number\n', source)
        assert returncode != 0
        assert 'invalid input' in out


def test_version():
    returncode, out, err = run_chef(['--version'])
    assert returncode == 0
    # argparse prints the version to stderr on Python 2 and to stdout on
    # Python 3
    assert out.strip() == 'chef 0.1' or err.strip() == 'chef 0.1'
