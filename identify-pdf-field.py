import argparse
import PyPDF2

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

def main():
    parser = argparse.ArgumentParser(description="Identify form fields in a PDF.")
    parser.add_argument("input_pdf", help="Input PDF file name")

    args = parser.parse_args()

    # Identify form fields
    form_fields = get_form_fields(args.input_pdf)

    # Generate command
    command = generate_command(args.input_pdf, form_fields)
    print(command)

if __name__ == "__main__":
    main()

