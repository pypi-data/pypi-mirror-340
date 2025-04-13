# Y-Translator CLI

An AI-powered command-line translator that converts between English and Chinese.

## Installation

```bash
pip install y-translator-cli
```

## Usage

Start the translator:
```bash
trans
```

Options:
- `-h, --help`: Show help message
- `-v, --version`: Show version information
- `--verbose`: Enable debug mode
- `--model MODEL`: Specify AI model to use (default: gpt-4)
- `--api-key KEY`: Set OpenAI API key
- `--api-base URL`: Set custom API base URL
- `-n, --no-stream`: Disable streaming mode

## Environment Variables

You can set the following environment variables:
- `AI_API_KEY`: Your OpenAI API key
- `AI_MODEL`: AI model to use (default: gpt-4)
- `AI_API_BASE`: Custom API base URL

## Examples

1. Start the translator:
```bash
trans
```

2. Enable debug mode:
```bash
trans --verbose
```

3. Use a specific model:
```bash
trans --model gpt-3.5-turbo
```

4. Disable streaming output:
```bash
trans -n
```

## Development

### Installation for Development

```bash
# Clone the repository
git clone https://github.com/yourusername/y-translator.git
cd y-translator

# Install in development mode
pip install -e .
```

### Building the Package

```bash
# Use build
python -m build
```

If building manually, you may want to clean old files first:
```bash
# Clean before building
rm -rf dist/ build/ *.egg-info/ __pycache__/ .pytest_cache/
find . -name "*.pyc" -delete
```

## License

MIT License 