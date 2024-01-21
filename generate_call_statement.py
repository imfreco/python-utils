import sys, re
file_name = sys.argv[1]
pattern = re.compile("([a-zA-Z0-9]{5,})")
match = pattern.search(file_name)
procedure_name = match.group()

with open(file_name, "r", encoding="utf-8") as file:
    file_lines = file.readlines()

input_params_keywords = "Parametros de entrada"
has_input_params = False
input_lines_indexes = {"first_line": 0, "last_line": 0}
is_input_indexes_setted = False
output_params_keywords = "Parametros de salida"
has_output_params = False
output_lines_indexes = {"first_line": 0, "last_line": 0}
is_output_indexes_setted = False
index = 0

for line in file_lines:
    if not is_input_indexes_setted:
        if not has_input_params and input_params_keywords in line:
            input_lines_indexes["first_line"] = index + 2
            has_input_params = True
        if has_input_params:
            if "-----" in line and index >= input_lines_indexes["first_line"]:
                input_lines_indexes["last_line"] = index - 1
                is_input_indexes_setted = True
            if index == len(file_lines) - 1:
                input_lines_indexes["last_line"] = index
                is_input_indexes_setted = True
    if is_input_indexes_setted and index - input_lines_indexes["last_line"] == 2 and output_params_keywords not in line:
        break
    if not has_output_params and output_params_keywords in line:
        output_lines_indexes["first_line"] = index + 3
        has_output_params = True
    if has_output_params:
        if "-----" in line and index >= output_lines_indexes["first_line"]:
            output_lines_indexes["last_line"] = index - 1
            break
        if index == len(file_lines) - 1:
            output_lines_indexes["last_line"] = index
    index += 1

call_statement = f'CALL {procedure_name}('

if(has_input_params):
    first_index = input_lines_indexes["first_line"]
    last_index = input_lines_indexes["last_line"]
    input_titles = file_lines[first_index:first_index + 1][0]
    idx = 0
    pointers = [0]
    last_char = ""

    for char in input_titles:
        if(last_char == " " and char != " "):
            pointers.append(idx)
        last_char = char
        idx += 1

    data_types, values = [], []
    for line in file_lines[first_index + 1:last_index + 1]:
        data_types.append(line[pointers[1]:pointers[2]].strip())
        values.append(line[pointers[3]:].strip())
        
    for index in range(len(values)):
        is_string = "CHAR" in data_types[index]
        if is_string:
            call_statement += "'"
        call_statement += values[index]
        if is_string:
            call_statement += "'"
        if index != len(values) - 1:
            call_statement += ", "

if(has_output_params):
    if(has_input_params):
        call_statement += ", "
    first_index = output_lines_indexes["first_line"]
    last_index = output_lines_indexes["last_line"]
    output_quant = last_index - first_index
    for index in range(output_quant + 1):
        call_statement += "null"
        if(index != output_quant):
            call_statement += ", "
        
call_statement += ");"

file_name_to_write = input("Case ID: ")
file = open(f'{file_name_to_write}.{file_name}.txt', 'w')
file.write(call_statement)
file.close()