# Python scripts to fill in pdf forms from command line or INI-style file (plus identifying fields in pdf forms)

## Overview

This directory contains two python scripts related to filling in pdf forms. 

The main tool aims to easily fill in a pdf form from  either the command line or by providing an INI-style file.

The easy part is filling in the form, and the tricky part (well, not that tricky) is to find out the names of the fields in the pdf file. This is the reason why we have another tool to ease the process of identifyiing the available files.


## Dependencies/prerequisites

These scripts require the `PyPDF2`, `configparser`, `argparse` and `unidecode` Python modules, that you can install using pip:

```bash
pip install PyPDF2 configparser argparse unidecode
    
done
```

It also uses a small module called `my_print_utils.py` that you can find in this very same directory.


## Tools

- `pdf-form-identify-fields.py`: This script identifies form fields in a PDF and generates:

   - A shell file with the command to fill them in. The command runs `pdf-form-fill.py` with command line arguments defining each 'field=value' pair
   - An INI file with the corresponding fields. It is also designed to be used by `pdf-form-fill.py`. 
   
   In both cases, the tool generates field values as placeholders in the form __FIELDNAME__, so that it can be further be used with additional scripts that run in batch mode doing simple substitutions.
   
   Do not panic when you see the field names in some pdf files, as pdf form designers do not think in providing nice concise names, but clearly understandable ones.

- `pdf-form-fill.py`: This script fills in form fields in a PDF. It can be used:

   - By running the shell script generated by `pdf-form-identify-fields.py`, after modifying the corresponding values.
   - By providing it with the INI file generated by `pdf-form-identify-fields.py`(after modifying the corresponding values), and/or command-line arguments defining the 'field=value' pairs.
   

## Usage

### Identify Form Fields

To identify form fields in a PDF, use the `pdf-form-identify-fields.py` script. For example:

```bash
python pdf-form-identify-fields.py my-form.pdf
```

This will generate a shell file that allows modification using a command in the shell, and also an INI file that can be further edited. To keep things simple, these files are named after the name of the pdf file, changing its extension to `.sh` and `.ini`, respectively. In the example these files would be `my_form.sh` and `my_form.ini`.



### Fill Form Fields

To fill form fields in a PDF, use the `pdf-form-fill.py` script. You can specify the field values as command-line arguments in `field_name=value` format, or you can provide an INI file with the 'field_name=value' pairs. If you don't specify an output PDF file name, the script will create a new PDF file with `-filled`` appended to the input PDF file name. You can also provide both an INI file and field definitions in the command line (command line field definitions override those found in the INI file, if the are found in both sources).

For example, to fill form fields using command-line arguments:

```bash
python pdf-form-fill.py my-form.pdf --field_values "field1=value1" "field2=value2"```
```

To fill form fields using an INI file:

```bash
python pdf-form-fill.py my-form.pdf --ini_file my-form.ini```
```

To fill form fields combining both:

```bash
python pdf-form-fill.py my-form.pdf --ini_file my-form.ini --field_values "field1=value1" "field2=value2"```
```

The INI file should have a [FormData] section with field_name=value entries. For example:

```ini
[FormData]
field1=value1
field2=value2
```


## Examples

In the directory `Forms-UAH` I include several PDF files used in my University, along with the INI and shell files generated by `pdf-form-identify-fields.py` with the following commands:

```bash
python ../pdf-form-identify-fields.py GEF06.pdf
python ../pdf-form-identify-fields.py GEF30.pdf
python ../pdf-form-identify-fields.py GEF07.pdf
python ../pdf-form-identify-fields.py GEF17.pdf
```

To use them, you just have to (for example for the `GEF07.pdf`):

- If you want to use the INI file:

  - Copy and edit the INI file with your data. If there is a field you don't want to fill in, just comment the line by inserting a `;` at the beginning of the corresponding line:
  
  ```bash
cp GEF07.ini GEF07-personal.ini
<edit command> GEF07-personal.ini
```

  - Run the pdf generation command to generate the customized file (named `20231123-GEF07-personal.pdf`):
  
```bash
python pdf-form-fill.py GEF07.pdf -i GEF07-personal.ini -o 20231123-GEF07-personal.pdf
```
  
- If you want to use the shell file, just edit it and run the pdf generation command:

```bash
cp GEF07.sh GEF-personal.sh
<edit command> GEF-personal.sh
bash GEF-personal.sh 
```

  In this case, the output file will be automatically named `GEF07-filled.pdf`.


## Note

These scripts are intended for use with simple PDF forms. They may not work correctly with complex forms that use JavaScript or other advanced features.


## TODO

Provide samples for batch processing using simple substitution of the value placeholders.

Provide high level tools to ease filling in known forms.


# Contributions/Help

If you need help to make this work, or you get any errors when running the tool, or even suggestions for improvements, or, better, want to contribute, please contact me at [my email address](mailto:javier.maciasguarasa@uah.es).

Enjoy!


Javi



