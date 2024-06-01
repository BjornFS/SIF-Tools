import re

from ..SIFplot import SIFplot
from .CommandLineInterface import CLI

class CLT:
    @staticmethod
    def process_input(user_input):
        def extract_command(user_input):
            commands = ["-plot", "-batch", "-hyperspectrum", "-convert", "-help"]
            for command in commands:
                if user_input.startswith(command):
                    remaining_input = user_input[len(command):].strip()
                    return command, remaining_input
            raise ValueError("Invalid command")
        
        def extract_args(user_input):
            reduce_noise_pattern = re.compile(r'-reduce_noise')
            window_pattern = re.compile(r'-window\s*=\s*(\w+)')

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
            parts = input_str.split()
            paths = []
            for part in parts:
                if part and not part.startswith('-'):
                    paths.append(part)
            return paths

        try:
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
                SIFplot.sif2csv(paths, loc)
        except ValueError as e:
            print(e)
