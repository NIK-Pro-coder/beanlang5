
from pathlib import Path
from termcolor import cprint

import toml
import sys

if len(sys.argv) > 1 :
	with open(sys.argv[1]) as f :
		raw_file = f.read()
else :
	print(
		"Syntax:",
		" beanlang [file]",
		"",
		"Options:",
		" -t, --save-tokens  Saves parsed tokens to tokens.json",
		sep = "\n"
	)
	exit(1)

class Config :
	def __init__(self, obj: dict) -> None:
		if not "main_dialect" in obj :
			cprint("Error: Config file does not specify a main dialect", "red")
			exit(1)

		self.main_dialect: str = obj["main_dialect"]

cprint("Loading config file...", "yellow", end = "\r")
with open(Path.home() / ".config/beanlang/config.toml") as f :
	config = Config(toml.load(f))
cprint("Successfully loaded config file!", "green")

from tokenParser import parseTokens

tokens = parseTokens(config.main_dialect, raw_file)
