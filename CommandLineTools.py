import re

from SIFplot import SIFplot
from CommandLineInterface import CLI

class CLT:
    """
    Command Line Tool (CLT) for processing user inputs related to SIF file operations.

    This class provides methods to process user commands for plotting, batch processing,
    hyperspectrum analysis, conversion, and displaying help information.
    """

    @staticmethod
    def process_input(user_input):
        """
        Process the user input command.

        Parameters
        ----------
        user_input : str
            The user input command as a string.

        Raises
        ------
        ValueError
            If the command is invalid.
        """
        
        def extract_command(user_input):
            """
            Extract the command from the user input.

            Parameters
            ----------
            user_input : str
                The user input command as a string.

            Returns
            -------
            tuple : (str, str)
                The extracted command and the remaining input.
            
            Raises
            ------
            ValueError
                If the command is invalid.
            """
            commands = ["-plot", "-batch", "-hyperspectrum", "-convert", "-help"]
            for command in commands:
                if user_input.startswith(command):
                    remaining_input = user_input[len(command):].strip()
                    return command, remaining_input
            raise ValueError("Invalid command")
        
        def extract_args(user_input):
            """
            Extract the arguments from the user input.

            Parameters
            ----------
            user_input : str
                The user input command as a string.

            Returns
            -------
            tuple : (dict, str)
                A dictionary of extracted arguments and the remaining input.
            """
            # Define the patterns to match
            reduce_noise_pattern = re.compile(r'-reduce_noise')
            window_pattern = re.compile(r'-window\s*=\s*(\w+)')

            # Search for the patterns in the input string
            reduce_noise_found = bool(reduce_noise_pattern.search(user_input))
            user_input = re.sub(reduce_noise_pattern, '', user_input).strip()
            
            window_match = window_pattern.search(user_input)
            window_value = window_match.group(1) if window_match else None
            user_input = re.sub(window_pattern, '', user_input).strip() if window_match else user_input

            return {
                "reduce_noise": reduce_noise_found,
                "window": window_value
            }, user_input

        def extract_paths(input_str):
            """
            Extract file paths from the remaining input.

            Parameters
            ----------
            input_str : str
                The remaining input after extracting command and arguments.

            Returns
            -------
            list : List[str]
                A list of file paths.
            """
            # Remaining parts are paths
            parts = input_str.split()
            paths = []
            for part in parts:
                if part and not part.startswith('-'):
                    paths.append(part)
            return paths

        command, reduced_input = extract_command(user_input)
        args, reduced_input = extract_args(reduced_input)
        paths = extract_paths(reduced_input)

        if command == "-help":
            CLI.display_help()
        elif command == "-plot":
            SIFplot.single(paths, window=args["window"], reduce_noise=args["reduce_noise"])
        elif command == "-batch":
            SIFplot.batch(paths)
        elif command == "-hyperspectrum":
            SIFplot.hyperspectrum(paths)
        elif command == "-convert":
            loc = input("Save to location: ")
            SIFplot.sif2array(paths, loc)