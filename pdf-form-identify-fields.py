# This script identifies form fields in PDF files and generates:
# - a shell script to fill them (This way you can edit the script to do the required modifications or use it as a
#   template to generate a script that will fill the form fields.
# - an INI file with the field names. This is useful to generate a template for the field values.

import argparse
import PyPDF2
import os
from unidecode import unidecode # This is used to remove accents from field names
from my_print_utils import print_err, print_inf, print_war

def get_form_fields2(input_pdf):
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        form_fields = reader.getFormTextFields()
        return form_fields

def get_form_fields(input_pdf):
    try:
        with open(input_pdf, 'rb') as file:
            reader = PyPDF2.PdfFileReader(file)
            form_fields = reader.getFormTextFields()
            return form_fields
    except FileNotFoundError:
        print_err(f"Error: The file '{input_pdf}' was not found.")
    except PyPDF2.errors.PdfReadError as e:
        print_err(f"Error reading the PDF file: {e}")
    except Exception as e:
        print_err(f"An unexpected error occurred: {e}")
    return None

def generate_command(input_pdf, form_fields):
    command_start = f"python pdf-form-fill.py {input_pdf} --field_values "
    # Generate field_command that will be a list of strings in the form '"field_name=__<field_name_without_spaces>__"'
    field_commands = [f"\"{field}=__{unidecode(field.replace(' ', '')).upper()}__\"" for field in form_fields]
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
            file.write(f"{field}=__{unidecode(field.replace(' ', '')).upper()}__\n")

def main():
    parser = argparse.ArgumentParser(description="Identify form fields in a PDF and generate a command to fill them.")
    parser.add_argument("input_pdf", help="Input PDF file name")
    parser.add_argument("-o", "--output_file", help="Output shell file to write the command (optional)", default=None)

    args = parser.parse_args()

    print(f"[INF] Identifying form fields in {args.input_pdf}...")
    # Identify form fields
    form_fields = get_form_fields(args.input_pdf)

    # Generate command
    command = generate_command(args.input_pdf, form_fields)

    # Write command to file or print it to the console
    if args.output_file:
        print(f"[INF] Writing command to {args.output_file}...")
        write_command_to_file(command, args.output_file)
    else:
        print(f"[INF] Command to fill form fields:\n{command}")

    # Write fields to INI file
    print(f"[INF] Writing field names to {os.path.splitext(args.input_pdf)[0]}.ini...")
    write_to_ini(args.input_pdf, form_fields)
    print("[INF] Done.")

if __name__ == "__main__":
    main()

