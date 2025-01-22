
import sys

def parseArgs(conv: dict[str, str]) -> tuple[dict, list[str]] :
	flags, args = {}, []

	inp = ""

	for i in sys.argv[1:] :
		if inp != "" :
			flags[inp] = i
			inp = ""
			continue

		if i.startswith("-") :
			if i.startswith("--") :
				flags[i[2:]] = None
				inp = i[2:]
			else :
				for l in i[1:] :
					flags[conv[l]] = None
					inp = conv[l]
		else :
			args.append(i)

	return flags, args
