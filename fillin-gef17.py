import argparse
import fitz  # PyMuPDF

def fill_pdf(input_pdf, output_pdf, field_values):
    # Open the PDF
    doc = fitz.open(input_pdf)

    # Iterate through each page and update fields
    for page_num in range(len(doc)):
        page = doc.loadPage(page_num)
        widgets = page.getWidgets()
        for widget in widgets:
            if widget.field_name in field_values:
                widget.set_text(field_values[widget.field_name])
                page.updateWidget(widget)
    
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

