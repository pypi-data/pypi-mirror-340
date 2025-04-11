# -*- coding: utf-8 -*-
import gears
from .core import GearsCore
from pathlib import Path
from rich.panel import Panel
from rich.console import Console
from argparse import ArgumentParser, Namespace

console: Console = Console()


# [CALL] get_cli
def get_cli() -> None:
    parser: ArgumentParser = ArgumentParser()
    parser.usage = "👉 gears [argument] [options]"
    parser.description = """Gears is an API Remote Code Executed (RCE)
    that serves as a bridge for beginners or developers, as a
    medium for learning coding.
Example:
    👉 gears <filename> | <strings> [options]
    👉 gears version // show Gears version info
    👉 gears list // show list available language"""
    parser.add_argument("resource", help="Running compile via File or String.")
    parser.add_argument(
        "-l",
        "--lang",
        help="The language flag is only available \
        for the String Resource type",
        type=str,
        default="unknown",
    )
    parser.add_argument(
        "-t",
        "--temp",
        help="there is an optional choice, whether to use a \
        temporary file or not by default false",
        type=bool,
        default=False,
    )
    parser.add_argument(
        "-v", "--verbose", help="show output details", type=bool, default=False
    )
    args: Namespace = parser.parse_args()

    match args.resource:
        case "version":
            console.print(
                f" 👉 [dark_orange]GearsCore@{gears.__version__} \
[blue](C) [reset]Aura Gears ID"
            )
        case "list":
            list_lang: str = (
                """[dark_orange]Cpp\tDart\tGo\tPython\tPhp\tLua
Ruby\tRust\tJs\tShell\tPerl\tElixir[reset]

Note: [grey50]always use --lang for string type sources"""
            )
            lang_support: Panel = Panel(list_lang)
            console.print(lang_support)
        case _:

            compilex: GearsCore = GearsCore(
                args.resource, language=args.lang, temp=args.temp
            )
            if args.verbose:
                verbose(compilex)
            else:
                console.print(
                    f"[magenta bold]Out [reset][green]> \
[reset]{compilex.output}"
                )


def verbose(object: GearsCore) -> None:
    filename: str = object.resource
    out: str = object.output
    err: str = object.error
    typeResource: str = object.type
    this_file: str = filename if Path(filename).is_file() else "~"
    message: str = ""
    if out != "":
        message = "Compiled successfully"
    else:
        message = "Failed to compile"

    console.print(
        Panel(
            f"""[dark_orange bold]Status [reset]: [green]{message}
[dark_orange bold]Source Type[reset]: [green]{typeResource}
[dark_orange bold]File [reset]: [green]{this_file}
[dark_orange bold]Output [reset]: [green]{out or err}""",
            title="Verboses Result",
        )
    )


def main() -> None:
    get_cli()


if __name__ == "__main__":
    main()
