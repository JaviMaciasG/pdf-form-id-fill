# Python scripts to identify fields in pdf forms and fill them easily (from command line/ini file)

## Overview

This directory contains Python scripts for working with PDF forms. The scripts allow you to identify form fields in a PDF, generate a command to fill them, and fill in the form fields with specified values.

## Files

- `pdf-form-identify-fields.py`: This script identifies form fields in a PDF and generates a command to fill them. It can write the command to a shell file or print it to the console, and an INI file with the corresponding fields, ready to be used by `pdf-form-fill.py`.

- `pdf-form-fill.py`: This script fills in form fields in a PDF. It can be used with the output of `pdf-form-identify-fields.py`, an INI file, or command-line arguments.

## Usage

### Identify Form Fields

To identify form fields in a PDF, use the `pdf-form-identify-fields.py` script. For example:

```bash
python pdf-form-identify-fields.py my-form.pdf
```

This will print a command to the console that you can use to fill the form fields. If you want to write the command to a shell file instead, use the -o option:

### Fill Form Fields

To fill form fields in a PDF, use the `pdf-form-fill.py` script. You can specify the field values as command-line arguments in field_name=value format, or you can provide an INI file with the field values. If you don't specify an output PDF file name, the script will create a new PDF file with -filled appended to the input PDF file name.  

For example, to fill form fields using command-line arguments:

```bash
python pdf-form-fill.py my-form.pdf --field_values "field1=value1" "field2=value2"```
```

To fill form fields using an INI file:

```bash
python pdf-form-fill.py my-form.pdf --ini_file my-form.ini```
```

The INI file should have a [FormData] section with field_name=value entries. For example:

```ini
[FormData]
field1=value1
field2=value2
```

## Dependencies

These scripts require the `PyPDF2`, `configparser` and `argparse` Python modules, tha you can install using pip:

```bash
pip install PyPDF2 configparser argparse
```

## Note

These scripts are intended for use with simple PDF forms. They may not work correctly with complex forms that use JavaScript or other advanced features.

