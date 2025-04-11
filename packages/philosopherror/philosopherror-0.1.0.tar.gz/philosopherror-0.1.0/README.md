# philosopherror

A silly yet insightful Python library that provides philosophical wisdom when errors and warnings occur.

## Overview

`philosopherror` enriches your debugging experience by adding philosophical quotes from both Eastern and Western philosophers whenever exceptions are raised or warnings are shown. It maps different error types to relevant philosophers, ensuring that the wisdom you receive is somewhat relevant to the error you're encountering.

## Features

* Automatically adds philosophical quotes to exceptions and warnings
* Maps specific error types to relevant philosophers
* Provides a decorator for adding philosophical wisdom to function errors
* Includes a direct API for accessing philosophical wisdom
* Can be enabled/disabled at runtime
* Contains genuine quotes from philosophers (no hallucinations)

## Installation

```bash
pip install philosopherror
```

## Usage

### Basic Usage

Simply import the library at the top of your script:

```python
import philosopherror
```

That's it! Now when errors occur, you'll get philosophical wisdom alongside them.

### Error Type Mapping

Different error types are mapped to philosophers whose wisdom might be relevant:

* Syntax errors: Wittgenstein, Confucius, Lao Tzu
* Logic errors: Aristotle, Kant, Plato
* Runtime errors: Seneca, Epictetus, Rumi
* System/IO errors: Marcus Aurelius, Rabindranath Tagore, Confucius

### Decorator

You can use the decorator to add philosophical wisdom to specific functions:

```python
@philosopherror.exception_handler
def risky_function():
    # This function might raise exceptions
    int("not a number")
```

### Direct API

```python
# Get wisdom from a specific philosopher
print(philosopherror.wisdom_from("Nietzsche"))

# Get random wisdom
print(philosopherror.random_wisdom())

# List all available philosophers
philosophers = philosopherror.list_philosophers()
```

### Enable/Disable

You can enable or disable the philosophical error messages at runtime:

```python
# Disable philosophical errors
philosopherror.disable()

# Re-enable philosophical errors
philosopherror.enable()
```

## Philosophers Included

### Western Philosophy
* Socrates, Plato, Aristotle
* Marcus Aurelius, Epictetus, Seneca
* Nietzsche, Kant, Wittgenstein
* Sartre, Camus

### Eastern Philosophy
* Confucius, Lao Tzu, Buddha
* Zhuangzi, Sun Tzu
* Rumi, Rabindranath Tagore, Alan Watts

### Indian Philosophy
* Swami Vivekananda, Sri Ramakrishna, Sri Aurobindo
* J. Krishnamurti, Ramana Maharshi, Adi Shankaracharya
* Paramahansa Yogananda, Kabir, Chanakya
* Thiruvalluvar, Jaggi Vasudev (Sadhguru)

## Example Output

```
Traceback (most recent call last):
  File "example.py", line 10, in <module>
    int("not a number")
ValueError: invalid literal for int() with base 10: 'not a number'

"The only true wisdom is in knowing you know nothing."
— Socrates
```

## Contributing

Feel free to contribute additional philosophers and quotes by submitting a pull request.

## License

MIT License