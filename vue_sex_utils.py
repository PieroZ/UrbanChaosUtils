import re
import statistics


def calc_xz_centre():
    sex_path = 'res/sex/roper.SEX'
    with open(sex_path, "r") as sex_file:
        sex_file_content = sex_file.readlines()
    # # Filter lines that start with "Vertex"
    # vertex_lines = [line.strip() for line in sex_file_content if line.startswith("Vertex")]
    #
    # print(vertex_lines)

    # Group consecutive "Vertex" lines together
    vertex_groups = []
    current_group = []
    previous_line_number = None

    for line_number, line in enumerate(sex_file_content):
        if line.startswith("Vertex"):
            if previous_line_number is not None and line_number != previous_line_number + 1:
                vertex_groups.append(current_group)
                current_group = []
            current_group.append((line_number, line.strip()))
            previous_line_number = line_number

    # Append the last group
    if current_group:
        vertex_groups.append(current_group)

    # Regular expression pattern to match vertex coordinates
    pattern = r"Vertex:\s*\(\s*(-?\d+\.\d+),\s*(-?\d+\.\d+),\s*(-?\d+\.\d+)\)"

    # Print vertex groups
    for group in vertex_groups:
        print("Group:")
        x_values = []
        y_values = []
        z_values = []
        for line_number, line in group:
            # print(f"  Line number: {line_number}, Content: {line}")
            # Extract x, y, and z values using regex
            match = re.match(pattern, line)
            if match:
                x_values.append(int(float(match.group(1)) * 256/100))
                y_values.append(int(float(match.group(2)) * 256/100))
                z_values.append(int(float(match.group(3)) * 256/100))

        print(x_values)
        print(int(statistics.fmean(x_values)))
        print(y_values)
        print(int(statistics.fmean(y_values)))
        print(z_values)
        print(int(statistics.fmean(z_values)))


def app():
    calc_xz_centre()


if __name__ == '__main__':
    app()
