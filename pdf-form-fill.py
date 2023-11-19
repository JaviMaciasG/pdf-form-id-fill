# This script fills in form fields in a PDF
# - It can be used with the output of pdf-form-identify-fields.py
# - It can also be used with an INI file, generated also by pdf-form-identify-fields.py

import argparse
import PyPDF2
import configparser
import os
from my_print_utils import print_err, print_inf, print_war

def fill_pdf(input_pdf, output_pdf, field_values):
    try:
        with open(input_pdf, 'rb') as file:
            reader = PyPDF2.PdfFileReader(file)
            writer = PyPDF2.PdfFileWriter()
            writer.cloneReaderDocumentRoot(reader)

            # Fill in the form fields
            for field_name, value in field_values.items():
                writer.updatePageFormFieldValues(reader.getPage(0), {field_name: value})

            # Write the output PDF file
            with open(output_pdf, 'wb') as output_file:
                writer.write(output_file)
        return True
    except IOError as e:
        print_err(f"IO Error while handling the file: {e}")
    except PyPDF2.errors.PdfReadError as e:
        print_err(f"Error reading the PDF file: {e}")
    except Exception as e:
        print_err(f"An unexpected error occurred: {e}")
    return False


def read_ini_file_orig(ini_file):
    config = configparser.ConfigParser()
    config.optionxform = str  # Preserve case of the keys, otherwise they are converted to lowercase

    config.read(ini_file)
    return {field: value for section in config.sections() for field, value in config.items(section)}

def read_ini_file(ini_file):
    config = configparser.ConfigParser()
    config.optionxform = str  # Preserve case of the keys, otherwise they are converted to lowercase

    try:
        with open(ini_file, 'r') as file:
            config.read_file(file)
        return {field: value for section in config.sections() for field, value in config.items(section)}
    except FileNotFoundError:
        print_err(f"Error: The INI file '{ini_file}' was not found.")
    except configparser.Error as e:
        print_err(f"Error parsing the INI file: {e}")
    except IOError as e:
        print_err(f"IO Error while reading the file: {e}")
    except Exception as e:
        print_err(f"An unexpected error occurred: {e}")
    return None


def main():
    parser = argparse.ArgumentParser(description="Fill fields in a PDF form.")
    parser.add_argument("input_pdf", help="Input PDF file name")
    parser.add_argument("-o", "--output-pdf", help="Output PDF file name (optional)", default=None)

    # Create a mutually exclusive group for -f and -i
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--field-values", nargs='+', help="Field values in 'field_name=value' format")
    group.add_argument("-i", "--ini-file", help="INI file with field values")

    args = parser.parse_args()

    print_inf(f"Running {os.path.basename(__file__)}")

    # If an INI file is provided, read values from it; otherwise, use command-line field values
    if args.ini_file: #and os.path.exists(args.ini_file):
        print_inf(f"Providing field values from ini file {args.ini_file}")
        field_values = read_ini_file(args.ini_file)
        if not field_values:
           print_err("Error reading ini file... exiting!")
           exit(4)
    else:
        print_inf(f"Providing field values from command line options...")
        field_values = {field.split('=')[0]: field.split('=')[1] for field in args.field_values}

    output_pdf = args.output_pdf if args.output_pdf else args.input_pdf.replace('.pdf', '-filled.pdf')
    print_inf(f"Writing provided field values to file {output_pdf}")
    if not fill_pdf(args.input_pdf, output_pdf, field_values):
       print_err("Error writing field values, exiting!")
       exit(2)

    print_inf(f"Done!")

    exit(0)

if __name__ == "__main__":
    main()

