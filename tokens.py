
from pathlib import Path

import json
import re

class Token :
	def __init__(self, obj, type) -> None:
		self.span: tuple[int, int] = obj.span()
		self.type: str = type
		self.value: str = obj.group()

	def __str__(self) -> str:
		return f"<Token value: '{self.value}', type: '{self.type}', span: {self.span}>"

def parseRule(rule: dict | list[str] | str) :
	if type(rule) is str :
		return {
			"rules": [rule],
			"child": {}
		}

	if type(rule) is list :
		return {
			"rules": rule,
			"child": {}
		}

	if type(rule) is dict :
		return {
			"rules": [rule["rule"]] if "rule" in rule else rule["rules"],
			"child": {x: rule["child"][x] for x in rule["child"]} if "child" in rule else {}
		}

	return {
		"rules": [],
		"child": {}
	}

def getMatching(pattern: str, string: str, type: str) -> list[Token] :
	found = [x for x in re.finditer(pattern, string)]
	got = [Token(x, type) for x in found]

	return got

def parseTokens(dialect_name: str, raw_text: str, save_tokens: bool = False) -> list[Token] :
	dialect = Path.home() / ".config/beanlang/dialects" / dialect_name

	with open(dialect / "rules.json") as f :
		dialect_rules = json.load(f)

	raw_text = raw_text.replace("\t", " ")

	tokens: list[Token] = []

	for i in dialect_rules :
		parsed = parseRule(dialect_rules[i])

		rules = parsed["rules"]

		for r in rules :
			found = getMatching(r, raw_text, i)

			for t in found :
				for l in parsed["child"] :
					if t.value in parsed["child"][l] :
						t.type = l

			tokens.extend(found)

	filled: list[bool] = [True for x in raw_text]

	new: list[Token] = []

	for i in tokens :
		pos = slice(*i.span)
		rng = range(*i.span)

		add = all(filled[pos])

		if add :
			new.append(i)
			for p in rng :
				filled[p] = False

	new.sort(key = lambda x: x.span[0])

	to_save: list = [{
		"value": x.value,
		"type": x.type,
		"span": x.span
	} for x in new]

	if save_tokens :
		with open("tokens.json", "w") as f :
			json.dump(to_save, f)

	return new
