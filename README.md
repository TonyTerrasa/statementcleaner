# statementcleaner
Small Python script that helps me clean csv downloads from my bank to the format I use for my budget spreadsheet. Sample budget spreadsheet [here](https://docs.google.com/spreadsheets/d/1jbjz7Cdj1VSFdF7fvUbAb35OGEwEfd6qp2VqAcJot_A/copy).

Currently can handle from: 
- Bank of America credit card
- USAA savings and checking accounts
- custom log I use for cash purchases

# Usage
```
usage: cleaner.py [-h] [--output OUTPUT] input_files [input_files ...]

convert a set of bank statements into the same csv format

positional arguments:
  input_files      List of input files to process

options:
  -h, --help       show this help message and exit
  --output OUTPUT  Output file (optional)
```


# Dependencies
Made with `Python 3.11`

Used Packages:
```
numpy==1.26.4
pandas==2.2.2
python-dateutil==2.9.0.post0
pytz==2024.1
six==1.16.0
tzdata==2024.1
```

