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
    command_start = f"python pdf-form-fill.py {input_pdf} --field-values "
    # Generate field_command that will be a list of strings in the form '"field_name=__<field_name_without_spaces>__"'
    field_commands = [f"\"{field}=__{unidecode(field.replace(' ', '')).upper()}__\"" for field in form_fields]
    command_body = " \\\n".join(field_commands)
    return command_start + command_body


def write_command_to_file(command, file_name):
    try:
        with open(file_name, 'w') as file:
            file.write(command + '\n')
        return True
    except IOError as e:
        print_err(f"Error writing to file {file_name}: {e}")
        return False

def write_to_ini(ini_filename, form_fields):
    try:
        with open(ini_filename, 'w') as file:
            file.write('[FormData]\n')
            for field in form_fields:
                file.write(f"{field}=__{unidecode(field.replace(' ', '')).upper()}__\n")
        return True
    except IOError as e:
        print_err(f"Error writing to file {ini_filename}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Identify form fields in a PDF and generate a command to fill them.")
    parser.add_argument("input_pdfs", nargs='+', help="Input PDF file name(s)")

    args = parser.parse_args()

    print_inf(f"Running {os.path.basename(__file__)} with input PDFs: {args.input_pdfs}")
    for input_pdf in args.input_pdfs:
        # Identify form fields in each PDF
        print_inf(f"Identifying form fields in {input_pdf}...")
        # Identify form fields
        form_fields = get_form_fields(input_pdf)
        if form_fields is None:
            print_err(f"Error getting form fields. Exiting.")
            break
        # Generate command
        command = generate_command(input_pdf, form_fields)
        # If an error occurred, break the loop
        if form_fields is None:
            print_war(f"Error generating shell file. Continuing...")
            break

        # print_inf(f"Command to fill form fields:\n{command}")

        # the output file will be named after the input file, with sh extension
        output_file = os.path.splitext(input_pdf)[0] + ".sh"
        print_inf(f"Writing command to {output_file}...")
        if not write_command_to_file(command, output_file):
            print_err(f"Error generating ini file. Continuing...")
            break
        else:
            print_inf("Now you can copy and edit the {output_file} with your data, and then run the fill in script:")
            print_inf(f" $ cp {output_file} my-{output_file}", cont=True)
            print_inf(f" $ <edit command> my-{output_file} ", cont=True)
            print_inf(f" $ bash my-{output_file}", cont=True)
            print_inf(f"And your pdf file will be {input_pdf.replace('.pdf', '-filled.pdf')}", cont=True)

        # Write fields to INI file
        ini_file = os.path.splitext(input_pdf)[0] + ".ini"
        print_inf(f"Writing field names to {ini_file}...")
        if not write_to_ini(ini_file, form_fields):
            print_err(f"Error writing field names to INI file. Continuing...")
            break
        else:
            print_inf("Now you can copy and edit the {ini_file} with your data, and then run the fill in script:")
            print_inf(f" $ cp {ini_file} my-{ini_file}", cont=True)
            print_inf(f" $ <edit command> my-{ini_file} ", cont=True)
            print_inf(f" $ python pdf-form-fill.py {input_pdf} -i my-{ini_file} -o my-{input_pdf}",
                      cont=True)
    print_inf("Done!")

if __name__ == "__main__":
    main()

