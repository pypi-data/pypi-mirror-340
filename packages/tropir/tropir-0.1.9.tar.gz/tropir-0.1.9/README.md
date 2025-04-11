# Tropir

A client for tracking LLM API calls and sending logs to your Tropir API.

## Installation

```bash
pip install tropir
```

## Usage

### Command Line Interface (Recommended)

Simply run your Python scripts or modules with the `tropir` command instead of `python`:

```bash
# Run a Python script with Tropir tracking
tropir python your_script.py

# Run a Python module with Tropir tracking
tropir python -m your_module
```

No code changes required! The Tropir agent automatically tracks all OpenAI API calls in your code.

### Advanced: As a Python Library

For more control, you can also use Tropir as a library:

```python
# Import and initialize the agent at the start of your program
from tropir import initialize
initialize()

# Now all your OpenAI API calls will be tracked automatically
```

## Configuration

Configuration is done via environment variables:

- `TROPIR_ENABLED`: Set to "0" to disable tracking (defaults to "1")
- `TROPIR_API_URL`: Custom API URL (defaults to "https://tropir.fly.dev/api/log")

## License

MIT 