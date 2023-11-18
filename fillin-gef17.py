import argparse
import PyPDF2

def fill_pdf(input_pdf, output_pdf, field_values):
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        writer = PyPDF2.PdfFileWriter()

        # Copy the contents of the input file to the writer
        writer.cloneReaderDocumentRoot(reader)

        # Fill in the form fields
        for field_name, value in field_values.items():
            writer.updatePageFormFieldValues(reader.getPage(0), {field_name: value})

        # Write the output PDF file
        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

def main():
    parser = argparse.ArgumentParser(description="Fill fields in a PDF form.")
    parser.add_argument("input_pdf", help="Input PDF file name")
    parser.add_argument("--output_pdf", help="Output PDF file name (optional)", default=None)
    parser.add_argument("--field_values", nargs='+', help="Field values in 'field_name=value' format", default=[])

    args = parser.parse_args()
    field_values = {field.split('=')[0]: field.split('=')[1] for field in args.field_values}
    output_pdf = args.output_pdf if args.output_pdf else args.input_pdf.replace('.pdf', '-filled.pdf')

    fill_pdf(args.input_pdf, output_pdf, field_values)

if __name__ == "__main__":
    main()

