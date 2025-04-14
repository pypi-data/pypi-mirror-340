import argparse
import asyncio
import sys
import termios
import tty
from functools import wraps
from typing import Any, Awaitable, Callable, Dict, Iterable, Optional

from pydantic import BaseModel


ANSI_COLORS = {
    'black': "\033[30m",
    'red': "\033[31m",
    'green': "\033[32m",
    'yellow': "\033[33m",
    'blue': "\033[34m",
    'magenta': "\033[35m",
    'cyan': "\033[36m",
    'white': "\033[37m",
    'reset': "\033[0m"
}

class CommandHandler:
    def __init__(self, callback: Callable[..., Awaitable[None]], parser: Optional[argparse.ArgumentParser] = None):
        self.callback = callback
        self.parser = parser


class CommandLineInterfaceConfig(BaseModel):
    """Pydantic model for configuring the Command Line Interface (CLI).

    Attributes:
        OUTPUT_LEVEL: Not implemented - planned for output filtering
        DIFFER_USERS_FROM_ITS_ROLES: Not implemented - user/role separation
        HASH_STORAGE_IN_RAM: Not implemented - credential storage control
        USER_ROLES: Not implemented - role-based access control
        PROMPT_DATA: Components for building colored prompts
        PROMPT_FORMAT_STRING: Format for combining prompt components
        ALLOW_BUILTIN_COMMANDS: Enable default exit/help commands
        ALLOW_DYNAMIC_PROMPTS: Not implemented - dynamic prompt changes
        ALLOW_ROUTING_OUTPUT: Not implemented - output redirection
        ALLOW_COMPLEX_COMMAND_CONVEYORS: Not implemented - command pipelines
        TERMINATE_ON_DISCONNECTION: Not implemented - session handling
        TRANSIENT_PROMPT: Clear input after submission
        TRANSIENT_MINI_PROMPT_COLOR: Color for transient prompt
        TRANSIENT_MINI_PROMPT: Alternate prompt in transient mode
        SUGGESTIONS_COLOR: Color for command suggestions
    """
    OUTPUT_LEVEL: str = 'ALL'
    DIFFER_USERS_FROM_ITS_ROLES: bool = False
    HASH_STORAGE_IN_RAM: bool = False
    USER_ROLES: Optional[list[str]] = None
    PROMPT_DATA: Optional[Dict[str, tuple[str, str]]] = None
    PROMPT_FORMAT_STRING: str = '>> '
    ALLOW_BUILTIN_COMMANDS: bool = True
    ALLOW_DYNAMIC_PROMPTS: bool = False
    ALLOW_ROUTING_OUTPUT: bool = False
    ALLOW_COMPLEX_COMMAND_CONVEYORS: bool = False
    TERMINATE_ON_DISCONNECTION: bool = True
    TRANSIENT_PROMPT: bool = False
    TRANSIENT_MINI_PROMPT_COLOR: str = 'white'
    TRANSIENT_MINI_PROMPT: str = '->'
    SUGGESTIONS_COLOR: str = 'blue'

class CommandRegistry:
    """Manages registration and lookup of command handlers."""

    def __init__(self):
        self.commands: Dict[str, CommandHandler] = {}

    def register(self, name, command: CommandHandler) -> None:
        """Register a new command handler.
            Args:
                name: Command name to register
                command: Handler implementation

            Raises:
                ValueError: If command name already exists
        """
        if name in self.commands:
            raise ValueError(f"Command {name} already registered")
        self.commands[name] = command

    def unregister(self, name: str) -> None:
        """Remove a command from the registry.
        Args:
            name: Command name to remove

        Raises:
            ValueError: If command doesn't exist
        """
        if name in self.commands:
            del self.commands[name]
        else:
            raise ValueError(f"Unknown command: {name}. Perhaps you should change it?")

    def get(self, name: str) -> Optional[CommandHandler]:
        """Retrieve a command handler by name."""
        return self.commands.get(name)

    def all(self) -> list:
        """Return all registered command handlers."""
        return list(self.commands.keys())

class LineEditor:
    """Handles line input editing with suggestions and transient prompts."""

    def __init__(
        self,
        prompt: str,
        mini_prompt: str,
        suggestions: list,
        suggestion_color: str,
        transient=False
    ):
        """
        Args:
            prompt: Main prompt text
            mini_prompt: Transient mode prompt
            suggestions: Initial command suggestions
            suggestion_color: ANSI color for suggestions
            transient: Enable transient prompt mode
        """
        self.transient = transient
        self.mini_prompt = mini_prompt
        self.prompt = prompt
        self.suggestion_color = suggestion_color
        self.suggestions = suggestions
        self.buffer = []
        self.cursor = 0
        self.original_settings = None
        self._suggested = False

    def _print_buffer(self) -> None:
        """Update terminal display with current input buffer."""
        if self._suggested:
            sys.stdout.write('\x1b[s\n\x1b[2K\x1b[u')
            sys.stdout.flush()
            self._suggested = False
        sys.stdout.write(f'\r{self.prompt}{"".join(self.buffer)} \r{self.prompt}{"".join(self.buffer[:self.cursor])}')
        sys.stdout.flush()

    def _suggest(self):
        """Display command suggestions based on current input."""
        prefix = ''.join(self.buffer)
        matches = [s for s in self.suggestions if s.startswith(prefix)]

        if len(matches) == 1:
            self.buffer = list(matches[0])
            self.cursor = len(self.buffer)
            self._print_buffer()
        elif len(matches) > 1 and self._suggested:
            self.buffer = list(matches[0])
            self.cursor = len(self.buffer)
            self._print_buffer()
        else:
            self._last_suggestion_lines = 1
            sys.stdout.write('\x1b[s')
            sys.stdout.write('\n')
            if matches:
                sys.stdout.write('[+] Possible suggestions: '
                                 + apply_color(', '.join(matches), self.suggestion_color))
            else:
                sys.stdout.write('[!] No suggestions')
            sys.stdout.write('\x1b[u')
            sys.stdout.flush()
            self._suggested = True

    def _enable_raw_mode(self):
        """Configure terminal for raw character input."""
        self.original_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())

    def _disable_raw_mode(self):
        """Restore original terminal settings."""
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.original_settings)

    async def readline(self) -> str:
        """Read a line of input with editing support.
        Returns:
            Entered command line as string
        """
        self.buffer = []
        self.cursor = 0

        self._enable_raw_mode()
        sys.stdout.write(self.prompt)
        sys.stdout.flush()

        try:
            while True:
                char = await asyncio.to_thread(sys.stdin.read, 1)

                if char == '\n':
                    if self.transient:
                        final_line = ''.join(self.buffer)
                        sys.stdout.write('\r\x1b[2K')
                        sys.stdout.write(self.mini_prompt + final_line + '\n')
                        sys.stdout.write('\x1b[2K')
                        sys.stdout.flush()
                        return final_line
                    else:
                        sys.stdout.write('\n')
                        return ''.join(self.buffer)
                elif char == '\x7f':
                    if self.cursor > 0:
                        self.cursor -= 1
                        self.buffer.pop(self.cursor)
                        self._print_buffer()
                elif char == '\t':
                    self._suggest()
                elif char == '\x03':
                    raise KeyboardInterrupt
                elif char == '\x1b':
                    next1 = await asyncio.to_thread(sys.stdin.read, 1)
                    next2 = await asyncio.to_thread(sys.stdin.read, 1)
                    if next1 == '[':
                        if next2 == 'C' and self.cursor < len(self.buffer):
                            self.cursor += 1
                        elif next2 == 'D' and self.cursor > 0:
                            self.cursor -= 1
                        self._print_buffer()
                else:
                    self.buffer.insert(self.cursor, char)
                    self.cursor += 1
                    self._print_buffer()
        finally:
            self._disable_raw_mode()

class CommandLineInterface:
    """Command line interface implementation handling input processing and command dispatch."""

    def __init__(self, config: CommandLineInterfaceConfig):
        """
        Args:
            config: Command line interface configuration parameters
        """

        self.prompt = None
        self.task = None
        self.should_close = False

        if config.PROMPT_DATA is not None:
            self.__build_prompt(
                prompt_data=config.PROMPT_DATA,
                format_string=config.PROMPT_FORMAT_STRING,
            )
        else:
            self.prompt = '>> '

        self.registry = CommandRegistry()
        self.editor = LineEditor(prompt=self.prompt, mini_prompt=config.TRANSIENT_MINI_PROMPT, suggestions=[],
                                 suggestion_color=config.SUGGESTIONS_COLOR, transient=config.TRANSIENT_PROMPT)

        if config.ALLOW_BUILTIN_COMMANDS:
            self.__register_builtins()


    def __register_builtins(self) -> None:
        """Register default commands (exit, all)."""
        async def exit_cli():
            self.should_close = True
        self.registry.register(name='exit', command=CommandHandler(exit_cli))
        async def print_all():
            await aprint(self.registry.all())
        self.registry.register(name='all', command=CommandHandler(print_all))


    def __build_prompt(self, prompt_data: dict[str, tuple[str, str]], format_string: str) -> None:
        """Construct colored prompt from components."""
        data_dict = {}
        for pair in prompt_data.items():
            data_dict[pair[0]] = apply_color(pair[1][0], pair[1][1])
        self.prompt = format_string.format(**data_dict)

    async def __run(self):
        """Main input processing loop."""
        self.editor.suggestions = self.registry.all()
        while not self.should_close:
            try:
                line = await self.editor.readline()
            except KeyboardInterrupt:
                await aprint("Terminating")
                break

            if not line:
                continue

            parts = line.split()
            cmd, args = parts[0], parts[1:]

            handler = self.registry.get(cmd)
            if not handler:
                await aprint(f"Unknown command: {cmd}")
                continue

            if handler.parser:
                try:
                    parsed_args = handler.parser.parse_args(args)
                    await handler.callback(**vars(parsed_args))
                except SystemExit:
                    handler.parser.print_help()
            else:
                await handler.callback()
            await asyncio.sleep(0.05)

    def command(self, arg_spec: Dict[str, Dict[str, Any]] = None):
        """
    Decorator to register a CLI command with argument parsing.

    The `arg_spec` dictionary defines the arguments and their settings,
    which will be used to build an `argparse.ArgumentParser` for the command.

    Args:
        arg_spec (dict): Specification of command-line arguments.
            Each key is the internal name of the argument passed to the function.
            Each value is a dictionary with optional keys:
                - flags (List[str]): Optional. CLI flags like ["-s", "--status"].
                                     If not provided, the argument is treated as positional.
                - type (Type):       Optional. Argument type, default is str.
                - choices (List):    Optional. Restricts the argument to specific values.
                - required (bool):   Optional. Whether the argument is required.
                                     Applies only to optional (flag-based) arguments.
                - nargs (str):       Optional. Accepts '?', '*', '+', etc. for multiple values.
                - help (str):        Optional. Description shown in --help output.
                - default:           Optional. Default value if argument is not provided.
                - action (str):      Optional. Special behavior modifier for flags. Useful for boolean or counting flags.
                                     Common values: "store", "store_true", "store_false", "count", "append", "help", "version".
    Notes:
        - All arguments defined in `arg_spec` must match function parameters by name.
        - This decorator automatically injects parsed arguments as keyword arguments.
        - Flags starting with `-` or `--` will be treated as optional;
          otherwise, arguments will be positional.
    """
        def decorator(func: Callable[..., Awaitable[Any]]):
            parser = None
            if arg_spec:
                parser = argparse.ArgumentParser(prog=func.__name__, add_help=True)
                for arg_name, options in arg_spec.items():
                    flags: Optional[Iterable] = options.pop('flags', None)

                    if flags:
                        parser.add_argument(*flags, dest=arg_name, **options)
                    else:
                        parser.add_argument(arg_name, **options)

            @wraps(func)
            async def wrapper(**kwargs):
                await func(**kwargs)

            self.registry.register(name=func.__name__, command=CommandHandler(wrapper, parser))
            return wrapper
        return decorator

    async def start(self) -> None:
        """Start interface."""
        self.task = asyncio.create_task(self.__run())
        await self.task

    async def stop(self) -> None:
        """Stop interface."""
        self.task.cancel()
        try:
            await self.task
        except asyncio.CancelledError:
            pass


#Helper functions
async def aprompt(prompt='>> ') -> str:
    """Asynchronous prompt for user input. Pending deprecation."""
    print(prompt, end='', flush=True)
    return (await asyncio.to_thread(sys.stdin.readline)).strip()

async def aprint(*args, sep=' ', end='\n', file=sys.stdout, flush=True) -> None:
    """Asynchronous print operation."""
    text = sep.join(map(str, args)) + end
    await asyncio.to_thread(file.write, text)
    if flush:
        await asyncio.to_thread(file.flush)

def apply_color(text: str, color: Optional[str]) -> str:
    """Apply ANSI color codes to text."""
    if color in ANSI_COLORS:
        return f"{ANSI_COLORS[color]}{text}{ANSI_COLORS['reset']}"
    return text

