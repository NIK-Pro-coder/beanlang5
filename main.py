
from pathlib import Path
from termcolor import cprint

import toml

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

print(config.main_dialect)
