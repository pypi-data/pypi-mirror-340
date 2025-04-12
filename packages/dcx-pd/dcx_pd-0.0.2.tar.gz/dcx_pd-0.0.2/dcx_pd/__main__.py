import code
import os
import pathlib as p
import re
import sys
from typing import Any

import arguably
import psutil
import rich
import rich.color
import rich.markup
import rich.table
import rich.text
from tcrutils.language import plural_s
from tcrutils.print import print_iterable
from tcrutils.rich import nay_print, nay_print_e, yay_print
from tcrutils.string import commafy

from dcx_pd import Export, __version__


def get_memory_usage_mb() -> float:
	process = psutil.Process(os.getpid())
	return process.memory_info().rss / 1024**2  # Convert bytes to MB


@arguably.command
def __root__(*paths: p.Path):
	"""\x1b[1mInteractively filter & search through a Discord Chat Exporter export.\x1b[0m

	Args:
		path: \x1b[1mPath to a Discord Chat Exporter export in `.json` format.\x1b[0m
	"""  # noqa: D400

	exports = []
	for path in paths:
		path = path.resolve()

		yay_print(
			f"[b][yellow]Loading [/][white]{rich.markup.escape(repr(path.name))}[/][yellow]...[/][/b]",
			escape_markup_obj=False,
		)

		try:
			if path.is_dir():
				raise IsADirectoryError

			exports.append(Export.from_path(path))
		except FileNotFoundError:
			nay_print(f"[b][red]File not found, [/red][white]{rich.markup.escape(path.__str__())}[/white][red], exiting... [/red][/b]", escape_markup_obj=False)
			return
		except IsADirectoryError:
			nay_print(f"[b][red]Path is a directory, [/][white]{rich.markup.escape(path.__str__())}[/][red], exiting...[/][/b]", escape_markup_obj=False)
			return
		except PermissionError:
			nay_print(f"[b][red]Permission denied, [/][white]{rich.markup.escape(path.__str__())}[/][red], exiting...[/][/b]", escape_markup_obj=False)
			return
		except OSError as e:
			if "Errno" not in str(e):
				e_str = str(e)
			else:
				e_str = str(e).split("Errno ")[1].split("]")[0].strip()

			nay_print(f"[b][red]Failed to load ({e_str}) [/][white]{rich.markup.escape(path.__str__())}[/][red], exiting...[/][/b]", escape_markup_obj=False)
			return

	yay_print(f"[b][yellow]Loaded [/][white]{commafy(n := sum(len(export.messages) for export in exports))}[/][yellow] message{plural_s(n)} ([/][white]mem: {get_memory_usage_mb():.2f}MB[/][yellow])[/][/b]", escape_markup_obj=False)

	context: dict[str, Any] = {
		"export": exports[0] if exports else None,
		"exports": exports,
		"re": re,
		"rich": rich,
	}

	sys.ps1 = "\x1b[1m>>> \x1b[0m"
	sys.ps2 = "\x1b[1m... \x1b[0m"
	sys.displayhook = lambda __o: print_iterable(__o, syntax_highlighting=True) if __o is not None else None

	try:
		yay_print("[b][yellow]Python [/][white]%s[/][yellow] on [/][white]%s[/][/]\n" % (sys.version, sys.platform), end="", escape_markup_obj=False)
		code.interact(banner="", local=context, exitmsg="")
	except SystemExit:
		pass


if __name__ == "__main__":
	arguably.run(
		version_flag=("-V", "--version"),
		show_types=False,
	)
