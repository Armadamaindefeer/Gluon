from library.cmdUtils.command import Shell, Command, Register, globalCommands
import library.cmdUtils.cmdUtils as cutils
from library.common import info, warn, error, SOURCE, getSource
import sys
import typing

def getAvailableToken(values:list[str],buffer:str):
	token_set = {token[:len(buffer)+1] for token in values if token.startswith(buffer)}
	if len(token_set) > 1 or len(token_set) == 0:
		return buffer
	else:
		returnToken = token_set.pop()
		available_value = [value for value in values if value.startswith(returnToken)]
		if len(available_value) == 1:
			return available_value[0] + " "
		else:
			return getAvailableToken(values,returnToken)

def autoComplete(char_buffer:str,values:list[str],alwaysShow=False) ->str:
	if not alwaysShow:
		display_token = [token for token in values if token.startswith(char_buffer)]
	else:
		display_token = values
	if len(display_token) > 1 and len(display_token) <= 60:
		print("\r",end="")
		for i,value in enumerate(display_token,1):
			terminator = "\n" if i % 6 == 0 else "\t"
			print(value,end=terminator)
		print()
	return getAvailableToken(values,char_buffer)

def autoCompleteFromToken(tokens:list[str],completionList:list[str],alwaysShow=False) -> str:
	if len(tokens) == 3 or (len(tokens) == 2 and tokens[1].count(" ") > 0):
		if len(tokens) == 2:
			result = autoComplete(tokens[-1],completionList,alwaysShow)
		else:
			result = autoComplete(tokens[-2],completionList,alwaysShow)
		if result.strip() == "":
			return "".join(tokens)
		else:
			return "".join([*tokens[:-2]," ",result])
	else:
		return "".join(tokens)

def autoCompleteFromList(completionList:list[str],alwaysShow=False) -> typing.Callable:
	def wrapped_autoComplete(tokens:list[str]):
		return autoCompleteFromToken(tokens,completionList,alwaysShow)
	return wrapped_autoComplete

def autoCompleteFromGen(completionGenFunc:typing.Callable,alwaysShow=False) -> typing.Callable:
	def wrapped_autoComplete(tokens:list[str]):
		return autoCompleteFromToken(tokens,completionGenFunc(),alwaysShow)
	return wrapped_autoComplete

@Register("exit","exit exitCode","exit application on use",optional=1) #TEXT
def _exit(input:Shell) -> None:
	exitCode:str = input[0] if len(input.input) > 0 else ""
	if cutils.Validate("Voulez vous quitter ?",SOURCE,enterIsYes=True): #TEXT
		sys.exit(exitCode)

@Register("help","help (TOPIC ENTRY)","Show help", optional=1,autoComplete=autoCompleteFromList(["Command"])) #TEXT
def _help(input:Shell) -> None:
	if len(input) == 0:
		for command in globalCommands:
			info("- " + command.syntax)
			info("\t" + command.desc)
			info("\tusage : "+ command.usage)

	if len(input) == 1:
		for command in globalCommands:
			if input[0] == command.syntax:
				info("- " + command.syntax)
				info("\t" + command.desc)
				info("\tusage : "+ command.usage)
				break
		else:
			error(f"Unrecognised commande : '{input[0]}'")
			return

