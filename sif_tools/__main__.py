from sif_tools.CommandLine.CommandLineTools import CLT
from sif_tools.CommandLine.CommandLineInterface import CLI

def main():
    """
    main for CLI
    """
    while True:
        run_program()

def run_program():
    CLI.intialise_program_window()
    CLI.display_program_header()
    CLI.display_program_info()
    CLI.display_commands()

    user_input = input("\n >>> ")
    CLT.process_input(user_input.strip())

if __name__ == "__main__":
    main()
