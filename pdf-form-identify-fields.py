# This script identifies form fields in a PDF and generates a command to fill them.
# Options
# -o, --output_file: Write the command to a shell file instead of printing it to the console
#   - This is useful if you want to edit the command before running it
#   - If you don't provide this option, the command will be printed to the console
#   - If you provide this option, the command will be written to the file you specify
#   - Example: python pdf-form-identify-fields.py my-form.pdf -o fill-my-form.sh

import argparse
import PyPDF2
import os
from unidecode import unidecode # This is used to remove accents from field names


def get_form_fields(input_pdf):
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        form_fields = reader.getFormTextFields()
        return form_fields

def generate_command(input_pdf, form_fields):
    command_start = f"python fill_script.py {input_pdf} --field_values "
    field_commands = [f'"{field}=YourValue"' for field in form_fields]
    command_body = " \\\n".join(field_commands)
    return command_start + command_body

def write_command_to_file(command, file_name):
    with open(file_name, 'w') as file:
        file.write(command + '\n')

def write_to_ini(input_pdf, form_fields):
    ini_filename = os.path.splitext(input_pdf)[0] + ".ini"
    with open(ini_filename, 'w') as file:
        file.write('[FormData]\n')
        for field in form_fields:
            file.write(f'{field}=YourValue\n')

def main():
    parser = argparse.ArgumentParser(description="Identify form fields in a PDF and generate a command to fill them.")
    parser.add_argument("input_pdf", help="Input PDF file name")
    parser.add_argument("-o", "--output_file", help="Output shell file to write the command (optional)", default=None)

    args = parser.parse_args()

    # Identify form fields
    form_fields = get_form_fields(args.input_pdf)

    # Generate command
    command = generate_command(args.input_pdf, form_fields)

    if args.output_file:
        write_command_to_file(command, args.output_file)
    else:
        print(command)

    # Write fields to INI file
    write_to_ini(args.input_pdf, form_fields)

if __name__ == "__main__":
    main()

