# coding: utf-8
from __future__ import with_statement

from collections import deque
from operator import add
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import pytest

from chef.interpreter import Interpreter, eval_instruction
from chef.datastructures import Ingredients, Ingredient, IngredientProperties
from chef.errors.runtime import InvalidInputError, UndefinedIngredientError,\
        InvalidContainerIDError, NonExistingContainerError,\
        EmptyContainerError, MissingLoopEndError


def instruction(command, lineno=1, **kwargs):
    d = {'command': command, 'lineno': lineno}
    d.update(kwargs)
    return d


def loop_start(verb, ingredient):
    return instruction('loop_start', verb=verb, ingredient=ingredient)


def loop_end(verb, ingredient=None):
    return instruction('loop_end', verb=verb, ingredient=ingredient)


def run(interpreter, instructions):
    'Execute `instructions` the way `interpret_recipe` does.'
    instructions = deque(instructions)
    while instructions:
        eval_instruction(instructions.popleft(), instructions, interpreter)


def test_interpreter_init():
    interpreter = Interpreter()
    assert interpreter.global_ingredients == Ingredients()
    assert interpreter.mixing_bowls == [Ingredients()]


class TestInterpreterProperties(object):
    def setup_method(self, method):
        first_mixing_bowl = Ingredients([
            Ingredient('apple', IngredientProperties(5, True, False)),
            Ingredient('water', IngredientProperties(100, False, True))])
        second_mixing_bowl = Ingredients([
            Ingredient('oil', IngredientProperties(2, True, False)),
            Ingredient('salmon', IngredientProperties(4, False, True))])
        self.interpreter = Interpreter(mixing_bowls=[
            first_mixing_bowl, second_mixing_bowl])

    def test_first_mixing_bowl(self):
        first_mixing_bowl = self.interpreter.first_mixing_bowl
        assert first_mixing_bowl == Ingredients([
            Ingredient('apple', IngredientProperties(5, True, False)),
            Ingredient('water', IngredientProperties(100, False, True))])

    def test_last_mixing_bowl(self):
        last_mixing_bowl = self.interpreter.last_mixing_bowl
        assert last_mixing_bowl == Ingredients([
            Ingredient('oil', IngredientProperties(2, True, False)),
            Ingredient('salmon', IngredientProperties(4, False, True))])


class TestInterpreterGetNthIngredients(object):
    params = {
        'test_lt_one': [{'id': -1}, {'id': 0}],
        'test_too_high': [{'id': 2}, {'id': 3}]}

    def setup_method(self, method):
        self.interpreter = Interpreter()

    def test_lt_one(self, id):
        with pytest.raises(InvalidContainerIDError):
            self.interpreter.get_nth_container(id)

    def test_too_high(self, id):
        with pytest.raises(NonExistingContainerError) as e:
            self.interpreter.get_nth_container(id)
        assert e.value.id == id

    def test_accessible(self):
        mixing_bowl = self.interpreter.get_nth_container(1)
        assert mixing_bowl == Ingredients()


class TestInterpreterTake(object):
    def setup_method(self, method):
        self.interpreter = Interpreter()

    def test_nonexisting(self):
        with pytest.raises(UndefinedIngredientError) as e:
            self.interpreter.take('milk', stdin=StringIO('23\n'))
        assert e.value.ingredient == 'milk'

    def test_overwriting(self):
        self.interpreter.global_ingredients['sausage'] = IngredientProperties(
            42, True, False)
        self.interpreter.take('sausage', stdin=StringIO('57\n'))
        sausage = self.interpreter.global_ingredients['sausage']
        assert sausage == Ingredient(
            'sausage', IngredientProperties(57, True, False))

    def test_invalid_num_without_lineno(self):
        with pytest.raises(InvalidInputError) as e:
            self.interpreter.take(
                'sausage', stdin=StringIO('not a number!\n'))
        assert e.value.value == 'not a number!'
        assert e.value.lineno is None

    def test_invalid_num_with_lineno(self):
        with pytest.raises(InvalidInputError) as e:
            self.interpreter.take(
                'sausage', 7, StringIO('not a number!\n'))
        assert e.value.value == 'not a number!'
        assert e.value.lineno == 7


class TestInterpreterPut(object):
    def setup_method(self, method):
        global_ingredients = Ingredients([
            Ingredient('bananas', IngredientProperties(180, True, False))])
        first_mixing_bowl = Ingredients([
            Ingredient('milk', IngredientProperties(200, False, True)),
            Ingredient('baking powder', IngredientProperties(50, True, False))])
        second_mixing_bowl = Ingredients([
            Ingredient('orange juice', IngredientProperties(100, False, True)),
            Ingredient('cinnamon', IngredientProperties(15, True, False))])
        self.interpreter = Interpreter(
            global_ingredients, [first_mixing_bowl, second_mixing_bowl])

    def test_undefined_ingredient(self):
        with pytest.raises(UndefinedIngredientError) as e:
            self.interpreter.put('olive oil')
        assert e.value.ingredient == 'olive oil'
        assert e.value.lineno is None

    def test_without_mixing_bowl(self):
        self.interpreter.put('bananas')
        assert self.interpreter.first_mixing_bowl.top == Ingredient(
            'bananas', IngredientProperties(180, True, False))

    def test_with_mixing_bowl(self):
        self.interpreter.put('bananas', 2)
        assert self.interpreter.mixing_bowls[1].top == Ingredient(
            'bananas', IngredientProperties(180, True, False))

    def test_into_nonexisting_mixing_bowl(self):
        self.interpreter.put('bananas', 3)
        assert self.interpreter.last_mixing_bowl == Ingredients([
            Ingredient('bananas', IngredientProperties(180, True, False))])
        assert self.interpreter.last_mixing_bowl.top == Ingredient(
            'bananas', IngredientProperties(180, True, False))

    def test_same_item_multiple_times(self):
        self.interpreter.put('bananas')
        assert self.interpreter.first_mixing_bowl == Ingredients([
            Ingredient('milk', IngredientProperties(200, False, True)),
            Ingredient('baking powder', IngredientProperties(50, True, False)),
            Ingredient('bananas', IngredientProperties(180, True, False))])
        self.interpreter.put('bananas')
        assert self.interpreter.first_mixing_bowl == Ingredients([
            Ingredient('milk', IngredientProperties(200, False, True)),
            Ingredient('baking powder', IngredientProperties(50, True, False)),
            Ingredient('bananas', IngredientProperties(180, True, False)),
            Ingredient('bananas', IngredientProperties(180, True, False))])

    def test_invalid_mixing_bowl(self):
        with pytest.raises(InvalidContainerIDError) as e:
            self.interpreter.put('bananas', 4)
        assert e.value.id == 4


class TestInterpreterFold(object):
    def test_missing_top_value(self):
        interpreter = Interpreter(
            Ingredients([
                Ingredient('yeast', IngredientProperties(47, True, False))]),
            [Ingredients()])
        with pytest.raises(EmptyContainerError) as e:
            interpreter.fold('yeast')
        assert e.value.id == 1

    def test_working(self):
        interpreter = Interpreter(
            Ingredients([
                Ingredient('yeast', IngredientProperties(47, True, False))]),
            [Ingredients([
                Ingredient('flour', IngredientProperties(23, True, False)),
                Ingredient('water', IngredientProperties(42, False, True))])])
        interpreter.fold('yeast')
        assert interpreter.mixing_bowls == [Ingredients([
            Ingredient('flour', IngredientProperties(23, True, False))])]
        # the value (and its state) of the popped ingredient is taken over
        assert interpreter.global_ingredients == Ingredients([
            Ingredient('yeast', IngredientProperties(42, False, True))])
        # the folded value is usable like any other ingredient
        interpreter.put('yeast')
        assert interpreter.first_mixing_bowl.top == Ingredient(
            'yeast', IngredientProperties(42, False, True))


def test_interpreter_calculate_with_empty_mixing_bowl():
    interpreter = Interpreter(Ingredients([
        Ingredient('pigs', IngredientProperties(2, True, False))]))
    with pytest.raises(EmptyContainerError):
        interpreter.calculate(add, 'pigs')


def test_interpreter_add(interpreter):
    assert interpreter.first_mixing_bowl.top == Ingredient(
        'cherries', IngredientProperties(300, True, False))
    interpreter.add('meat')
    assert interpreter.first_mixing_bowl.top == Ingredient(
        'meat', IngredientProperties(350, True, False))


def test_interpreter_remove(interpreter):
    assert interpreter.first_mixing_bowl.top == Ingredient(
        'cherries', IngredientProperties(300, True, False))
    interpreter.remove('meat')
    assert interpreter.first_mixing_bowl.top == Ingredient(
        'meat', IngredientProperties(250, True, False))


def test_interpreter_combine(interpreter):
    assert interpreter.first_mixing_bowl.top == Ingredient(
        'cherries', IngredientProperties(300, True, False))
    interpreter.combine('meat')
    assert interpreter.first_mixing_bowl.top == Ingredient(
        'meat', IngredientProperties(15000, True, False))


def test_interpreter_divide(interpreter):
    assert interpreter.first_mixing_bowl.top == Ingredient(
        'cherries', IngredientProperties(300, True, False))
    interpreter.divide('meat')
    assert interpreter.first_mixing_bowl.top == Ingredient(
        'meat', IngredientProperties(6, True, False))


def test_interpreter_liquefy_ingredient(interpreter):
    assert interpreter.global_ingredients == Ingredients([
        Ingredient('meat', IngredientProperties(50, True, False))])
    interpreter.liquefy_ingredient('meat')
    assert interpreter.global_ingredients == Ingredients([
        Ingredient('meat', IngredientProperties(50, False, True))])


def test_interpreter_liquefy_contents(interpreter):
    assert interpreter.first_mixing_bowl == Ingredients([
        Ingredient('apples', IngredientProperties(100, True, False)),
        Ingredient('ketchup', IngredientProperties(200, False, True)),
        Ingredient('cherries', IngredientProperties(300, True, False))])
    interpreter.liquefy_contents()
    assert interpreter.first_mixing_bowl == Ingredients([
        Ingredient('apples', IngredientProperties(100, False, True)),
        Ingredient('ketchup', IngredientProperties(200, False, True)),
        Ingredient('cherries', IngredientProperties(300, False, True))])


def test_interpreter_stir_minutes(interpreter):
    interpreter.stir_minutes(1)
    assert interpreter.first_mixing_bowl == Ingredients([
        Ingredient('apples', IngredientProperties(100, True, False)),
        Ingredient('cherries', IngredientProperties(300, True, False)),
        Ingredient('ketchup', IngredientProperties(200, False, True))])


def test_interpreter_stir_ingredient():
    interpreter = Interpreter(
        Ingredients([
            Ingredient('sticks', IngredientProperties(2, True, False))]),
        [Ingredients([
            Ingredient('stones', IngredientProperties(100, True, False)),
            Ingredient('skin', IngredientProperties(200, True, False)),
            Ingredient('bones', IngredientProperties(300, True, False))])])
    interpreter.stir_ingredient('sticks')
    assert interpreter.first_mixing_bowl == Ingredients([
        Ingredient('bones', IngredientProperties(300, True, False)),
        Ingredient('stones', IngredientProperties(100, True, False)),
        Ingredient('skin', IngredientProperties(200, True, False))])


def test_interpreter_clean(interpreter):
    interpreter.clean()
    # global ingredients must not change after having called the clean command
    assert interpreter.global_ingredients == Ingredients([
        Ingredient('meat', IngredientProperties(50, True, False))])
    assert interpreter.mixing_bowls == [Ingredients()]


def test_interpreter_pour(interpreter):
    assert interpreter.first_baking_dish == Ingredients()
    interpreter.pour()
    assert interpreter.first_baking_dish == Ingredients([
        Ingredient('apples', IngredientProperties(100, True, False)),
        Ingredient('ketchup', IngredientProperties(200, False, True)),
        Ingredient('cherries', IngredientProperties(300, True, False))])


class TestInterpreterLoopStart(object):
    def setup_method(self, method):
        global_ingredients = Ingredients([
            Ingredient('number', IngredientProperties(3, True, False))])
        self.interpreter = Interpreter(global_ingredients)

    def test_one_iteration(self):
        interpreter = Interpreter(
            Ingredients([
                Ingredient('number', IngredientProperties(1, True, False))]))
        following_instructions = deque([
            {
                'command': 'put',
                'ingredient': 'number',
                'mixing_bowl_id': None,
                'lineno': 8},
            {
                'command': 'loop_end',
                'ingredient': 'number',
                'verb': 'counted',
                'lineno': 9}])
        interpreter.loop_start('Count', 'number', following_instructions, 7)
        assert interpreter.first_mixing_bowl == Ingredients([
            Ingredient('number', IngredientProperties(1, True, False))])

    def test_multiple_iterations(self):
        following_instructions = deque([
            {
                'command': 'put',
                'ingredient': 'number',
                'mixing_bowl_id': None,
                'lineno': 8},
            {
                'command': 'loop_end',
                'ingredient': 'number',
                'verb': 'counted',
                'lineno': 9}])
        self.interpreter.loop_start(
            'Count', 'number', following_instructions, 7)
        assert self.interpreter.first_mixing_bowl == Ingredients([
            Ingredient('number', IngredientProperties(3, True, False)),
            Ingredient('number', IngredientProperties(2, True, False)),
            Ingredient('number', IngredientProperties(1, True, False))])

    def test_nested_loops(self):
        interpreter = Interpreter(Ingredients([
            Ingredient('i', IngredientProperties(2, True, False)),
            Ingredient('j', IngredientProperties(2, True, False)),
            Ingredient('x', IngredientProperties(7, True, False))]))
        run(interpreter, [
            loop_start('Analyze', 'i'),
            loop_start('Examine', 'j'),
            instruction('put', ingredient='j'),
            loop_end('examined', 'j'),
            instruction('put', ingredient='x'),
            loop_end('analyzed', 'i'),
            instruction('put', ingredient='x')])
        # `j` is never reset, so the inner loop runs only in the first
        # iteration of the outer loop
        assert [(i.name, i.properties.value)
                for i in interpreter.first_mixing_bowl] == [
            ('j', 2), ('j', 1), ('x', 7), ('x', 7), ('x', 7)]

    def test_body_is_not_executed_again_after_the_loop(self):
        interpreter = Interpreter(Ingredients([
            Ingredient('number', IngredientProperties(2, True, False)),
            Ingredient('marker', IngredientProperties(0, True, False))]))
        run(interpreter, [
            loop_start('Count', 'number'),
            instruction('put', ingredient='number'),
            loop_end('counted', 'number'),
            instruction('put', ingredient='marker')])
        assert [(i.name, i.properties.value)
                for i in interpreter.first_mixing_bowl] == [
            ('number', 2), ('number', 1), ('marker', 0)]

    def test_loop_is_skipped_if_the_value_is_zero(self):
        interpreter = Interpreter(Ingredients([
            Ingredient('number', IngredientProperties(0, True, False)),
            Ingredient('marker', IngredientProperties(5, True, False))]))
        run(interpreter, [
            loop_start('Count', 'number'),
            instruction('put', ingredient='number'),
            loop_end('counted', 'number'),
            instruction('put', ingredient='marker')])
        assert [(i.name, i.properties.value)
                for i in interpreter.first_mixing_bowl] == [('marker', 5)]

    def test_missing_loop_end(self):
        following_instructions = deque([
            {
                'command': 'put',
                'ingredient': 'number',
                'mixing_bowl_id': None,
                'lineno': 8},
            {
                'command': 'add',
                'ingredient': 'number',
                'mixing_bowl_id': None,
                'lineno': 9}])
        with pytest.raises(MissingLoopEndError):
            self.interpreter.loop_start(
                'Count', 'number', following_instructions, 7)


def test_interpreter_loop_end(interpreter):
    interpreter.loop_end('meat')
    assert interpreter.global_ingredients == Ingredients([
        Ingredient('meat', IngredientProperties(49, True, False))])


def test_interpreter_serves():
    interpreter = Interpreter()
    interpreter.baking_dishes = [Ingredients([
        Ingredient('water', IngredientProperties(97, False, True)),
        Ingredient('salt', IngredientProperties(23, True, False)),
        Ingredient('magic powder', IngredientProperties(55000, False, True))])]
    stdout = StringIO()
    interpreter.serves(1, stdout)
    stdout.seek(0)
    output = stdout.read()
    assert output == '훘23a'


def test_interpreter_calculate_replaces_the_top_ingredient():
    interpreter = Interpreter(
        Ingredients([
            Ingredient('a', IngredientProperties(10, True, False))]),
        [Ingredients([
            Ingredient('a', IngredientProperties(1, True, False)),
            Ingredient('b', IngredientProperties(2, True, False))])])
    interpreter.add('a')
    assert interpreter.first_mixing_bowl == Ingredients([
        Ingredient('a', IngredientProperties(1, True, False)),
        Ingredient('a', IngredientProperties(12, True, False))])


def test_interpreter_liquefy_contents_with_duplicate_names():
    interpreter = Interpreter(
        Ingredients(),
        [Ingredients([
            Ingredient('a', IngredientProperties(1, True, False)),
            Ingredient('a', IngredientProperties(2, True, False))])])
    interpreter.liquefy_contents()
    assert interpreter.first_mixing_bowl == Ingredients([
        Ingredient('a', IngredientProperties(1, False, True)),
        Ingredient('a', IngredientProperties(2, False, True))])


def test_interpreter_mix(interpreter):
    before = list(interpreter.first_mixing_bowl)
    interpreter.mix()
    assert sorted(interpreter.first_mixing_bowl) == sorted(before)


def test_eval_stir_minutes(interpreter):
    eval_instruction(
        instruction('stir_minutes', minutes=1, mixing_bowl_id=None),
        deque(), interpreter)
    assert interpreter.first_mixing_bowl == Ingredients([
        Ingredient('apples', IngredientProperties(100, True, False)),
        Ingredient('cherries', IngredientProperties(300, True, False)),
        Ingredient('ketchup', IngredientProperties(200, False, True))])
