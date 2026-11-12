# chef

An interpreter for the esoteric programming language
[Chef](https://www.dangermouse.net/esoteric/chef.html), written in Python.

In Chef, programs look like cooking recipes. Ingredients are variables,
mixing bowls and baking dishes are stacks, and the method steps are the
instructions.

## Installation

```sh
pip install .
```

Python 3.10 or newer is required.

## Usage

```sh
chef -f examples/helloworld.chef
```

Options:

| Option             | Description                               |
| ------------------ | ----------------------------------------- |
| `-f`, `--file`     | path to the Chef file to parse/evaluate   |
| `-p`, `--parse-only` | only parse the program, do not run it   |
| `--version`        | show the version and exit                 |

## Example

`examples/helloworld.chef` is a fruit salad that prints a greeting:

```
Fruit salad.

Ingredients.
72 bananas
101 oranges
108 apples
...

Method.
Put lychees into mixing bowl.
Put strawberries into mixing bowl.
...
```

More examples (`loop.chef`, `nested_loop.chef`, `simple_nested_loop.chef`)
are in the [`examples`](examples) directory.

## Development

Tests use [pytest](https://pytest.org) with `pytest-cov` and are run across
interpreters with [tox](https://tox.wiki):

```sh
tox
# or, in a single environment:
pytest --cov chef chef/tests
```

Project layout:

- `bin/chef` – command line entry point
- `chef/parser.py` – parses Chef recipes
- `chef/interpreter.py` – evaluates parsed recipes and implements the CLI
- `chef/datastructures.py`, `chef/validators.py`, `chef/utils.py` – helpers
- `chef/errors/` – syntax and runtime errors
- `chef/tests/` – test suite

## License

ISC. Copyright Simon Liedtke.
