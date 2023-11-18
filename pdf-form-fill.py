# This script fills in form fields in a PDF
# - It can be used with the output of pdf-form-identify-fields.py
# - It can also be used with an INI file, generated also by pdf-form-identify-fields.py

import argparse
import PyPDF2
import configparser
import os

def fill_pdf(input_pdf, output_pdf, field_values):
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

def read_ini_file(ini_file):
    config = configparser.ConfigParser()
    config.optionxform = str  # Preserve case of the keys, otherwise they are converted to lowercase
    config.read(ini_file)
    return {field: value for section in config.sections() for field, value in config.items(section)}

def main():
    parser = argparse.ArgumentParser(description="Fill fields in a PDF form.")
    parser.add_argument("input_pdf", help="Input PDF file name")
    parser.add_argument("--output_pdf", help="Output PDF file name (optional)", default=None)
    parser.add_argument("--field_values", nargs='+', help="Field values in 'field_name=value' format", default=[])
    parser.add_argument("--ini_file", help="INI file with field values (optional)", default=None)

    args = parser.parse_args()

    # If an INI file is provided, read values from it; otherwise, use command-line field values
    if args.ini_file and os.path.exists(args.ini_file):
        field_values = read_ini_file(args.ini_file)
    else:
        field_values = {field.split('=')[0]: field.split('=')[1] for field in args.field_values}

    output_pdf = args.output_pdf if args.output_pdf else args.input_pdf.replace('.pdf', '-filled.pdf')
    fill_pdf(args.input_pdf, output_pdf, field_values)

if __name__ == "__main__":
    main()

