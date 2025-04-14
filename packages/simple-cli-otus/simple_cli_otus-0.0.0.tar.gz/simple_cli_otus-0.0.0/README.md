# Simple CLI

Asynchronous framework in which you can create interactive command line interfaces with:
- Dynamic completion
- Color schemes
- Customizable prompts


## Quick start

### Installation 
```bash
pip install simple-cli-otus
```
### Basic usage

```python

from SimpleCLI import CommandLineInterface, CommandLineInterfaceConfig
import asyncio

config = CommandLineInterfaceConfig(
    PROMPT_FORMAT_STRING=">>> ",
    TRANSIENT_PROMPT=True,
    SUGGESTION_COLORS="green"
)

cli = CommandLineInterface(config)

@cli.command()
async def hello(name: str = "world"):
    """User greeting."""
    print(f"Hello, {name}!")

@cli.command(arg_spec={
    'status': {
        'flags': ['-s', '--status'],
        'help': "Some status.",
        'action': 'store_true'
    }
})
async def check(status: bool = False):
    """System checkup"""
    if status:
        print("System: OK")
    else:
        print("No status provided")

# Running interface
async def main():
    await cli.start()
    await cli.stop()
if __name__ == "__main__":
    asyncio.run(main())
```
### Features
- ANSI color schemes
- Autosuggestion by Tab
- Asynchronous operations
- Configuration via Pydantic-model

### Restrictions
Some configuration features are not implemented yet:
- User role model
- Output routing
- Command conveyors
- Log filtering

## Development

Clone repository and install in development mode:
```bash
git clone https://github.com/MartisCoding/SimpleCLI
cd SimpleCLI
pip install -e .[dev]
```

## License
This project was developed under MIT Licence. 



