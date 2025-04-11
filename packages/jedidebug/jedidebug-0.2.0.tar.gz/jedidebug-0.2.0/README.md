# JediDebug

A Python library that motivates programmers with Star Wars quotes when bugs occur. May the Force be with your debugging!

## Overview

JediDebug is a lighthearted Python library that catches exceptions and provides motivational Star Wars-themed wisdom. Perfect for keeping spirits high during frustrating debugging sessions and adding a touch of the Force to your development workflow.

## Features

* Automatically adds Star Wars quotes to exceptions
* Provides a decorator for adding Jedi wisdom to function errors
* Includes quotes from various Star Wars characters and films
* Can be enabled/disabled at runtime
* Supports custom Jedi quotes and categories

## Installation

```bash
pip install jedidebug
```

## Usage

### Basic Usage

Simply import the library and activate the Jedi wisdom:

```python
from jedidebug import JediDebug

# Activate the Jedi wisdom globally
JediDebug.activate()

# Now any unhandled exception will trigger a motivational Star Wars quote
def broken_function():
    return 1 / 0

try:
    broken_function()
except:
    pass  # The exception will be printed with Jedi wisdom
```

### Function Decorator

You can use the decorator to add Jedi wisdom to specific functions:

```python
from jedidebug import JediDebug

# Only provide Jedi guidance for specific functions
@JediDebug.jedi_function
def another_broken_function():
    x = [1, 2, 3]
    return x[10]  # Index error

try:
    another_broken_function()
except:
    pass  # This function will receive Jedi wisdom
```

### Getting Quotes Directly

```python
# Get a random quote
wisdom = JediDebug.get_motivational_quote()
print(wisdom)

# Get wisdom from a specific category (if available)
wisdom = JediDebug.get_quote_by_category('debugging')
print(wisdom)
```

### Customizing Quotes

You can add your own Star Wars quotes to the library:

```python
from jedidebug import JediDebug

# Add custom quotes
JediDebug.add_quotes([
    "The bug is strong with this one.",
    "You were the chosen one! You were supposed to destroy the bugs, not create them!",
])

# Add categorized quotes
JediDebug.add_categorized_quotes('syntax', [
    "The syntax is strong with this one, but your brackets are not.",
    "Your indentation has strayed to the dark side.",
])
```

### Enable/Disable

You can enable or disable the Jedi wisdom at runtime:

```python
# Disable Jedi wisdom
JediDebug.deactivate()

# Re-enable Jedi wisdom
JediDebug.activate()
```

## Sample Output

```
Traceback (most recent call last):
  File "example.py", line 10, in <module>
    broken_function()
  File "example.py", line 7, in broken_function
    return 1 / 0
ZeroDivisionError: division by zero

✨ JEDI WISDOM ✨
🌟 I find your lack of comments disturbing.
🌟 Trust your instincts, young Padawan. The solution is near.
```

## Quote Categories

JediDebug includes quotes for different error scenarios:

* General debugging wisdom
* Logic errors
* Syntax issues
* Runtime problems
* And more!

## Why Use JediDebug?

* To add some fun to your debugging process
* To maintain motivation during frustrating bug hunts
* To bring the wisdom of Star Wars to your development workflow
* Because even Jedi Masters encounter bugs in their code

## Contributing

Feel free to contribute additional Star Wars quotes or features by submitting a pull request.

## License

MIT License