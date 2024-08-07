import re
import pyperclip


def convert_defines_to_static_const_int(input_text):
    # Regex to match define statements
    define_pattern = re.compile(r'#define\s+(\w+)\s+(\d+)')
    output_lines = []

    for line in input_text.splitlines():
        match = define_pattern.match(line)
        if match:
            # Extract the name and value
            name, value = match.groups()
            # Convert to static const int
            output_lines.append(f'static const int {name} = {value};')
        else:
            output_lines.append(line)

    return "\n".join(output_lines)


def main():
    try:
        # Try to read from the clipboard
        input_text = pyperclip.paste()
        if input_text.strip() == "":
            raise ValueError("Clipboard is empty. Switching to file input mode.")
    except Exception as e:
        print(str(e))
        # If clipboard reading fails, read from a file
        input_file = 'input.txt'
        with open(input_file, 'r') as f:
            input_text = f.read()

    output_text = convert_defines_to_static_const_int(input_text)
    print(output_text)

    # Optionally, copy the result back to the clipboard
    try:
        pyperclip.copy(output_text)
    except Exception as e:
        print(f"Could not copy to clipboard: {str(e)}")


if __name__ == "__main__":
    main()
