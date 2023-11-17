import argparse
import fitz  # PyMuPDF

def fill_pdf(input_pdf, output_pdf, field_values):
    # Open the PDF
    doc = fitz.open(input_pdf)

    # Iterate through each page and fill in the fields
    for page in doc:
        for field in field_values:
            try:
                page[0][field] = field_values[field]
            except KeyError:
                print(f"Field '{field}' not found in the PDF.")

    # Save the filled PDF
    doc.save(output_pdf)
    doc.close()

def main():
    # Set up argparse for command line arguments
    parser = argparse.ArgumentParser(description="Fill fields in a PDF form.")
    parser.add_argument("input_pdf", help="Input PDF file name")
    parser.add_argument("--output_pdf", help="Output PDF file name (optional)", default=None)
    parser.add_argument("--field_values", nargs='+', help="Field values in 'field_name=value' format", default=[])

    args = parser.parse_args()

    # Parse field values
    field_values = {field.split('=')[0]: field.split('=')[1] for field in args.field_values}

    # Default output filename if not provided
    output_pdf = args.output_pdf if args.output_pdf else args.input_pdf.replace('.pdf', '-filled.pdf')

    # Fill the PDF
    fill_pdf(args.input_pdf, output_pdf, field_values)

if __name__ == "__main__":
    main()

