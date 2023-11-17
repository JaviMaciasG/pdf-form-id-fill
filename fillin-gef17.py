import argparse
import pdfrw

def fill_pdf(input_pdf, output_pdf, field_values):
    template = pdfrw.PdfReader(input_pdf)
    annotations = template.Root.Pages.Kids[0].Annots  # Assuming fields are on the first page

    for annotation in annotations:
        if annotation.Subtype == '/Widget' and annotation.T:
            field_name = annotation.T[1:-1]  # Remove parentheses
            if field_name in field_values:
                annotation.update(
                    pdfrw.PdfDict(V='{}'.format(field_values[field_name]))
                )

    pdfrw.PdfWriter().write(output_pdf, template)

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

