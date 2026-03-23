#!/usr/bin/env python3
from sys import argv
from os import listdir, getcwd, system, path
from os.path import isfile, join

def get_all_files_in_dir(path: str) -> list:
	# only_files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
	only_files = [f for f in listdir(path) if isfile(join(path, f))]
	return only_files

def get_last_accessed_file(files: list[str]) -> str:
	last_time = None
	last_file = None
	for file_path in files:
		curr_time = path.getatime(file_path)
		if last_time:
			if curr_time > last_time:
				last_time = curr_time
				last_file = file_path
		else:
			last_time = curr_time
			last_file = file_path
	return last_file

def prompt_for_lines() -> tuple[int]:
	start = input("Enter Starting Line: ").strip()
	end = input("Enter Ending Line: ").strip()
	return (start, end)

def display_help():
	system('clear')
	message = "Kaveh's Line Copy Tool USAGE:"
	print(message, '\n', len(message)*"-", sep='')
	print("\tlin_cpy <None>")
	print("\t\t(default)")
	print("\t\tcopies specified lines from last opened file in current directory\n")
	print("\tlin_cpy <file_name>")
	print("\t\tcopies specified lines from <file_name>\n")

def main():

	argc = len(argv)
	execute = True

	if argc == 1:
		message = "WELCOME to Kaveh's Vim Line Copy TOOL"
		print(message, "\n", len(message)*"=", sep='')

		current_path = getcwd()
		all_files = get_all_files_in_dir(current_path)
		last_file = get_last_accessed_file(all_files)
		file_name = last_file
		print(f"currently selected file: {file_name}\n")
		start_line, end_line = prompt_for_lines()
	else:
		arg = argv[1]
		if arg == '-h' or arg == '--h' or arg == '-help' or arg == '--help':
			execute = False
			display_help()
		else:
			message = "WELCOME to Kaveh's Vim Line Copy TOOL"
			print(message, "\n", len(message)*"=", sep='')
			start_line, end_line = prompt_for_lines()
			file_name = argv[1]

	if execute:
		command = f"sed -n '{start_line},{end_line}p' {file_name} | xclip -selection clipboard"
		system(command)

if __name__ == "__main__":
	main()
