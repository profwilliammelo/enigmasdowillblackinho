import os

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# The file currently starts with the broken dictionary content.
# We need to find where the NEXT question starts or where the list continues.
# Looking at previous view_file, line 1 was "pergunta": "Sobre..."
# This corresponds to the first question.
# We want to skip this first broken question because header_temp.py has it.

# Let's find the start of the second question or the end of the first.
# The first question ends at line 9 with "}," in the previous view.
# So we should probably skip the first 9 lines.

rest_of_code = lines[9:] 

with open('header_temp.py', 'r', encoding='utf-8') as f:
    header = f.read()

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(header)
    f.writelines(rest_of_code)

print("Fixed app.py")
