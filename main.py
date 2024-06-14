from abc import abstractmethod
import argparse
import re
import sys

#No use of Machine argument or STDIN input - unsure of the required implementation
#Start position is not included in the output, unsure of which value its looking for.
#Design Structure I choose to use was Strategy 
# It is a behavioral design pattern that turns a set of behaviors into objects and makes them interchangeable inside original context object.

def main():
    # Parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--regex', required=True)
    parser.add_argument('-f', '--files', nargs='*')
    parser.add_argument('-u', '--underscore', action='store_true')
    parser.add_argument('-c', '--color', action='store_true')
    #unsued argument
    parser.add_argument('-m', '--machine', action='store_true')
    
    args = parser.parse_args()

    if args.underscore:
        formatter = UnderscoreFormatter()
    elif args.color:
        formatter = ColorFormatter()
    else:
        formatter = DefaultFormatter()

    regex = re.compile(args.regex)
    
    if args.files:
        for file in args.files:
            search_in_file(file, regex, formatter)


def search_in_file(file_name, regex, formatter):
    try:
        with open(file_name, 'r') as f:
            for line_num, line in enumerate(f, start=1):
                matches = list(regex.finditer(line))
                if matches:
                    formatter.format(file_name, line_num, line, matches)
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
    except Exception as e:
        print(f"Error processing file '{file_name}': {e}")

# Class that handles the output formatting - must be implemented by subclasses
# https://docs.python.org/3/library/abc.html - Abstract Base Classes
class OutputFormatter:
    @abstractmethod
    def format(file_name, line_num, line, matches):
        raise NotImplementedError("Must be implemented by subclasses")

class UnderscoreFormatter(OutputFormatter):
    def format(self, file_name, line_num, line, matches):
        prefix = f"{file_name}:{line_num}:"
        print(f"{prefix}{line.strip()}")
        
        underline = [' '] * (len(prefix) + len(line.strip()))
        
        for match in matches:
            # Adjust to account for the prefix length
            start = match.start() + len(prefix)
            end = match.end() + len(prefix)
            for i in range(start, end):
                underline[i] = '^'
        print(''.join(underline))
        
class DefaultFormatter(OutputFormatter):
    def format(self, file_name, line_num, line, matches):
        print(f"{file_name}:{line_num}:{line.strip()}")

#Class that handles the color formatting - each match is highlighted in red
class ColorFormatter(OutputFormatter):
    def format(self, file_name, line_num, line, matches):
        start_color = '\033[31m'
        end_color = '\033[0m'
        output = line
        offset = 0
        for match in matches:
            start = match.start() + offset
            end =  match.end() + offset
            output = output[:start] + start_color + output[start:end] + end_color + output[end:]
            offset += len(start_color) + len(end_color)
        print(f"{file_name}:{line_num}:{output.strip()}")

if __name__ == '__main__':
    main()