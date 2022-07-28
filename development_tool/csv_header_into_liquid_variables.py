import re


def convert_header(string_header, string_row_variable, delimiter):
    result = "{" + f"%- assign header_item = {string_row_variable} | string.strip_newlines | string.strip  | string.split '{delimiter}' -%" + "}\n\n"

    for i, field in enumerate(string_header.split(delimiter)):
        field = field.lower()
        field = field.strip().replace(" ", "_").replace("(", "").replace(")", "").replace(".", "").replace("-", "_")
        field = re.sub("[0-9]_", "", field)
        result += "{" + f"%- assign {field} = header_item[{i}] -%" + "}\n"

    print(result)  # todo display in interface
