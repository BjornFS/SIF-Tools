import os, sys

class CLI:
    """
    Command Line Interface (CLI) for displaying program information and handling user inputs.

    This class provides methods to initialize the program window, display headers, 
    program information, available commands, help information, and handle file selection.
    """
    @staticmethod
    def intialise_program_window():
        """
        Clear the console window.
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def display_program_header():
        """
        Display the program header.
        """
        header = (
            "                     _            _____                         \n"
            "     /\             | |          |  __ \                        \n"
            "    /  \   _ __   __| | ___  _ __| |__) |_ _ _ __ ___  ___ _ __ \n"
            "   / /\ \ | '_ \ / _` |/ _ \| '__|  ___/ _` | '__/ __|/ _ \ '__|\n"
            "  / ____ \| | | | (_| | (_) | |  | |  | (_| | |  \__ \  __/ |   \n"
            " /_/    \_\_| |_|\__,_|\___/|_|  |_|   \__,_|_|  |___/\___|_|   \n"
            "                                                                \n"
            "                                                                "
        )
        print(header)

    @staticmethod
    def display_program_info():
        """
        Display information about the program.
        """
        print("\nThis software is released under MPL-2.0")
        print("May 2024 \t Version 1.1")
        print("Author: Bjørn Funch Schrøder Nielsen @ bjornfschroder@gmail.com\n")
        print("--- A program to read and plot Andor Technology Multi-Channel files (.sif) ---\n")

    @staticmethod
    def display_commands():
        """
        Display the available commands.
        """
        print("Available commands:")
        print("[help]\t\t\t-help")
        print("[plot]\t\t\t-plot")
        print("[batchjob]\t\t-batch")
        print("[hyperspectrum]\t\t-hyperspectrum")
        print("[sif-2-csv]\t\t-convert")
    
    @staticmethod
    def display_help():
        """
        Display help information for the available commands.
        """
        CLI.intialise_program_window()
        CLI.display_program_header()
        
        help_text = """
        ============================================================
                               Help Information
        ============================================================

        Read & plot Andor Technology Multi-Channel files (.sif).
        The paths to the .sif files can be written out explicitly, 
        or dragged and dropped into the command-line.

        Below are the available commands and their usage:

        1. -help
           :: Displays this help information.

        2. -plot <file_path1> <file_path2> ...
           :: Plots one (or more) .sif file(s) in the same fig.

        3. -batch <file_path1> <file_path2> ...
           :: Plots multiple .sif files in separate plots.

        4. -hyperspectrum <file_path1> <file_path2> ...
           :: Performs hyperspectrum analysis on a collection .sif files

        5. -convert <file_path1> <file_path2> ...
           :: Converts one (or more) .sif file(s) to arrays and 
           saves them in the .csv file format.
           After executing this command, the user will be prompted for a
           path to save the file(s) to.
        """
        print(help_text)
        input("\nPress any key to return to menu...")

    @staticmethod
    def display_files(position, files):
        """
        Display a list of files with a selector.

        Parameters
        ----------
        position : int
            The current position of the selector.
        
        files : List[str]
            A list of file names to display.
        """
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
        CLI.display_program_header()
        print('Select background data:\n')

        for index, filename in enumerate(files):
            if index == position:
                print(f"> {filename}")
            else:
                print(f"  {filename}")
        print("\n")
        
    def get_key():
        """
        Get a key press from the user.

        Returns
        -------
        str
            The key pressed by the user. Possible values are 'UP', 'DOWN', 'ENTER'.
        """
        if os.name == 'nt':
            import msvcrt
            while True:
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    if key == b'\xe0':  # Special keys (arrows, f keys, ins, del, etc.)
                        key = msvcrt.getch()
                        if key == b'H':  # Up arrow
                            return 'UP'
                        elif key == b'P':  # Down arrow
                            return 'DOWN'
                    elif key == b'\r':  # Enter key
                        return 'ENTER'
        else:
            import tty
            import termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            if ch == '\x1b':  # Escape sequence
                ch += sys.stdin.read(2)
                if ch == '\x1b[A':  # Up arrow
                    return 'UP'
                elif ch == '\x1b[B':  # Down arrow
                    return 'DOWN'
            elif ch == '\r':  # Enter key
                return 'ENTER'

    def menu_select(files):
        """
        Display a menu to select a file.

        Parameters
        ----------
        files : List[str]
            A list of file names to display.

        Returns
        -------
        str
            The selected file name.
        """
        position = 0
        while True:
            CLI.display_files(position, files)
            key = CLI.get_key()
            print(key)
            if key == 'UP' and position > 0:
                position -= 1
            elif key == 'DOWN' and position < len(files) - 1:
                position += 1
            elif key == 'ENTER':
                break
        return files[position]