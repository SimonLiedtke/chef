# coding: utf-8
import os
from io import StringIO

import pytest

from chef.datastructures import Ingredient, IngredientProperties, Ingredients
from chef.interpreter import Interpreter

RECIPE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'recipes'))


def pytest_generate_tests(metafunc):
    # parametrize the test functions of classes which have a `params`
    # attribute (a dictionary which maps the name of a test function to a
    # list of dictionaries with the arguments of one call of the function)
    params = getattr(metafunc.cls, 'params', {})
    calls = params.get(metafunc.function.__name__)
    if calls:
        argnames = sorted(calls[0])
        metafunc.parametrize(
            argnames, [[call[name] for name in argnames] for call in calls])


@pytest.fixture
def interpreter():
    return Interpreter(
        Ingredients([
            Ingredient('meat', IngredientProperties(50, True, False))]),
        [Ingredients([
            Ingredient('apples', IngredientProperties(100, True, False)),
            Ingredient('ketchup', IngredientProperties(200, False, True)),
            Ingredient('cherries', IngredientProperties(300, True, False))])])


@pytest.fixture
def ingredients():
    return Ingredients([
        Ingredient('sugar', IngredientProperties(120, True, False)),
        Ingredient('water', IngredientProperties(250, False, True))])


@pytest.fixture
def fp_with_one_blank_line():
    return StringIO('1st\n2nd\n3rd\n\n4th\n5th\n')


@pytest.fixture
def fp_with_two_blank_lines():
    return StringIO('1st\n2nd\n3rd\n\n4th\n5th\n\n6th\n7th\n')


@pytest.fixture
def fp_without_any_blank_line():
    return StringIO('1st\n2nd\n3rd\n')


@pytest.fixture
def missing_method_recipe():
    return StringIO('''A recipe which misses the method element.

the comment

not-a-method''')


@pytest.fixture
def multiple_instr():
    return StringIO('''A recipe with more than one instruction.

Method.
Put sugar into mixing bowl.
Liquefy sugar.
Pour contents of the mixing bowl into the baking dish.''')

# valid recipes:
#  1. only title and methods √
#  2. everything
#  3. only descr. √
#  4. only ingredients √
#  5. only cooking time √
#  6. only oven temp. √
#  7. only serves √
#  8. only descr. and ingredients √
#  8. only descr. and cooking time √
#  9. only descr. and oven temp. √
# 10. only descr. and serves √
# 11. ingredients and cooking time √
# 12. ingredients and oven temp. √
# 13. ingredients and serves √
# 14. cooking time and oven temp. √
# 15. cooking time and serves √
# 16. oven temp. and serves √
# 17. descr., ingredients and cooking time √
# 18. descr., ingredients and oven temp. √
# 19. descr., ingredients and serves √
# 17. descr., cooking time and oven temp. √
# 18. descr., cooking time and serves √
# 19. descr., oven temp. and serves √
# 20. ingredients, cooking time and oven temp. √
# 21. ingredients, cooking time and serves √
# 22. cooking time, oven temp. and serves √
# 23. descr., ingredients, cooking time and oven temp. √
# 24. descr., ingredients, cooking time and serves √
# 25. descr., ingredients, oven temp. and serves √
# 26. descr., cooking time, oven temp. and serves √
# 27. ingredients, cooking time, oven temp. and serves √
# 28. descr., ingredients, cooking time, oven temp. and serves?


@pytest.fixture
def only_title_and_method():
    return StringIO('''A very basic recipe.

Method.
Take apple from refrigerator.''')


@pytest.fixture
def description_only():
    return StringIO('''A recipe with some text.

This paragraph explains the recipe. It does not have real content here,
because its only purpose in this recipe is to test whether comments are
detected correctly or not. I will write some more sentences just for fun
and because paragraphs usually consists of more than just one sentence.
So here comes another sentence. And one more.

Method.
Take apple from refrigerator.''')


@pytest.fixture
def ingredients_only():
    return StringIO('''A recipe with an ingredient list.

Ingredients.
108 g lard
111 cups oil

Method.
Take apple from refrigerator.''')


@pytest.fixture
def cooking_time_only():
    return StringIO('''A meal which has to be cooked 20 minutes.

Cooking time: 20 minutes.

Method.
Take apple from refrigerator.''')


@pytest.fixture
def oven_temp_only():
    return StringIO('''A recipe which requires baking.

Pre-heat oven to 200 degrees Celsius (gas mark 5).

Method.
Take apple from refrigerator.''')


@pytest.fixture
def serves_only():
    return StringIO('''The meal which is only served, not made.

Method.
Take apple from refrigerator.

Serves 4.''')


@pytest.fixture
def description_and_ingredients():
    return StringIO('''Gnocchi Mac and Cheese.

This is a really simple and reduced form of the recipe I found at
http://www.thejeyofcooking.com/gnocchi-mac-and-cheese/.

Ingredients.
1 kg gnocchi
2 tablespoons butter
1 tablespoon flour
1 cup milk
4 cups cheese

Method.
Take apple from refrigerator.''')


@pytest.fixture
def description_and_cooking_time():
    return StringIO('''Cooked apple.

A recipe where one is supposed to take out an apple from the refrigerator and
cook it for two hours. Quite strange, but that doesn't matter :)

Cooking time: 2 hours.

Method.
Take apple from refrigerator.''')


@pytest.fixture
def description_and_oven_temp():
    return StringIO('''Wasted energy.

This is a recipe where the oven is pre-heated, but not used afterwards. What a
waste of energy!

Pre-heat oven to 250 degrees Celsius (gas mark 7).

Method.
Take apple from refrigerator.''')


@pytest.fixture
def description_and_serves():
    return StringIO('''A recipe for five.

This is a recipe for five people. They should not be hungry, because all they
can get is an apple which comes from a refrigerator.

Method.
Take apple from refrigerator.

Serves 5.''')


@pytest.fixture
def ingredients_and_cooking_time():
    return StringIO('''Some strane tuna salad.

Ingredients.
72 kg tuna
2300 g lettuce
37 cups olive oil
18 peppers

Cooking time: 10 minutes.

Method.
Take apple from refrigerator.''')


@pytest.fixture
def ingredients_and_oven_temp():
    return StringIO('''Something typical American.

Ingredients.
1 kg marshmallows
5 bananas
3 cups hazelnuts
500 g chocolate

Pre-heat oven to 220 degrees Celsius.

Method.
Take apple from refrigerator.''')


@pytest.fixture
def ingredients_and_serves():
    return StringIO('''Little food for many people.

Ingredients.
2 ml water
13 raisins
6 ml rum

Method.
Take apple from refrigerator.

Serves 23.''')


@pytest.fixture
def cooking_time_and_oven_temp():
    return StringIO('''Untitled.

Cooking time: 45 minutes.

Pre-heat oven to 250 degrees Celsius (gas mark 5).

Method.
Take apple from refrigerator.''')


@pytest.fixture
def cooking_time_and_serves():
    return StringIO('''An apple for singles.

Cooking time: 15 minutes.

Method.
Take apple from refrigerator.

Serves 1.''')


@pytest.fixture
def oven_temp_and_serves():
    return StringIO('''A meal for eight apple lovers.

Pre-heat oven to 175 degrees Celsius.

Method.
Take apple from refrigerator.

Serves 8.''')


@pytest.fixture
def descr_ingr_cooking_time():
    return StringIO('''Apple dessert.

This is a simple recipe.

Ingredients.
apple
2 teaspoons cinnamon
1 teaspoons brown sugar

Cooking time: 20 minutes.

Method.
Take apple from refrigerator.''')


@pytest.fixture
def descr_ingr_oven_temp():
    return StringIO('''Dessert with oranges and vanilla ice cream.

I have written enough recipes to be out of creativity now. So here's no text
which explains this recipe but some words to show how much I lack of
creativity.

Ingredients.
100 ml water
3 oranges
2 dashes lemon juice
250 ml vanilla ice cream

Pre-heat oven to 250 degrees Celsius.

Method.
Take apple from refrigerator.''')


@pytest.fixture
def descr_ingr_serves():
    return StringIO('''A satanic soup for witches and wizards.

Don't try this at home. Seriously.

Ingredients.
7 frog legs
23 g spiders
13 zombie brains
200 ml werewolf blood

Method.
Take apple from refrigerator.

Serves 12.''')


@pytest.fixture
def descr_cooking_time_oven_temp():
    return StringIO('''Cook and pre-heat, look but don't eat.

Bla bla bla.

Cooking time: 15 minutes.

Pre-heat oven to 200 degrees Celsius.

Method.
Take apple from refrigerator.''')


@pytest.fixture
def descr_cooking_time_serves():
    return StringIO('''Bla bla bla.

yada yada.

Cooking time: 7 hours.

Method.
Take apple from refrigerator.

Serves 5.''')


@pytest.fixture
def descr_oven_temp_serves():
    return StringIO('''Nothing.

We pre-heat the oven, but don't put anything into it. Waste ALL the energy!
Recipe was written for one person, so double the temperature for two persons!

Pre-heat oven to 80 degrees Celsius (gas mark 2).

Method.
Take apple from refrigerator.

Serves 1.''')


@pytest.fixture
def ingr_cooking_time_oven_temp():
    return StringIO('''Pickles 'n' wheat.

Ingredients.
5 pickles
200 g wheat

Cooking time: 25 minutes.

Pre-heat oven to 220 degrees Celsius.

Method.
Take apple from refrigerator.''')


@pytest.fixture
def ingr_cooking_time_serves():
    return StringIO('''2 girls, 1 cup.

Ingredients.
2 girls
1 cup chocolate

Cooking time: 1 minute.

Method.
Take apple from refrigerator.

Serves 2.''')


@pytest.fixture
def cooking_time_oven_temp_serves():
    return StringIO('''Da da daa.

Cooking time: 2 hours.

Pre-heat oven to 130 degrees Celsius.

Method.
Take apple from refrigerator.

Serves 7.''')


@pytest.fixture
def descr_ingr_cooking_time_oven_temp():
    return StringIO('''Yeuks.

Bla bla bla, yada yada.

Ingredients.
25 l beer
5 pinches mustard

Cooking time: 34 minutes.

Pre-heat oven to 85 degrees Celsius.

Method.
Take apple from refrigerator.''')


@pytest.fixture
def descr_ingr_cooking_time_serves():
    return StringIO('''Screeeeeek.

A description of the very important recipe. Here another sentence of those I
am tired of inventing.

Ingredients.
2 dashes oil
4 kg potatoes

Cooking time: 3 hours.

Method.
Take apple from refrigerator.

Serves 4.''')


@pytest.fixture
def descr_ingr_oven_temp_serves():
    return StringIO('''Water and buns.

Yep, that's it.

Ingredients.
1 l water
6 buns

Pre-heat oven to 120 degrees Celsius.

Method.
Take apple from refrigerator.

Serves 6.''')


@pytest.fixture
def descr_cooking_time_oven_temp_serves():
    return StringIO('''Bla bla.

Yada yada.

Cooking time: 17 minutes.

Pre-heat oven to 220 degrees Celsius (gas mark 7).

Method.
Take apple from refrigerator.

Serves 2.''')


@pytest.fixture
def ingr_cooking_time_oven_temp_serves():
    return StringIO('''yoghurt & bacon.

Ingredients.
100 ml yoghurt
50 g bacon

Cooking time: 25 minutes.

Pre-heat oven to 175 degrees Celsius (gas mark 5).

Method.
Take apple from refrigerator.

Serves 10.''')


@pytest.fixture
def invalid_code():
    return StringIO('''valid title.

a perfectly fine description follows.

but then: bam! some words that the parser can't handle!''')
