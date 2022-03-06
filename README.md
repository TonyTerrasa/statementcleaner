# statementcleaner
Small Python script that helps me clean csv downloads from my bank to the format I use for my budget spreadsheet

The two banks I'm currently using and Bank of America and Santander (Spain). This script takes in the a csv exported from either of these two banks and transforms it into a format which is conveient for my own personal purchase log in my budget

# Usage
```
usage: cleaner.py [-h] -file FILE [-output OUTPUT] [-type {bofa,santander}]

optional arguments:
  -h, --help            show this help message and exit
  -file FILE, -f FILE   location of the input file
  -output OUTPUT, -o OUTPUT
                        location of the output file
  -type {bofa,santander}, -t {bofa,santander}
                        type of bankstatement
```

# Specifications 

## Bank of America

Reads statement from the Bank of America web page exported as 
"Microsoft Excel Format" (which is actually in csv format)

Output columns of this format are: 
`Posted Date,Reference Number,Payee,Address,Amount`

Function performs the following transformation of header names 
and returns pandas dataframe
```
Posted Date -> Date (keep the same)
Reference Number -> [Delete]
Payee -> Name
Address -> [Delete]
[Add] Category -> "" for all 
[Add] Unit -> "USD" for all 
Amount -> [same, but converted to positive number]
```

Finally, any entries that say "PAYMENT - THANK YOU" are removed as they're not useful for me in keeping track of my expenses


## Santander (Es)
Reads statement from the Spanish version of the Santander web 
page exported as "Exportar Excel"

Output columns of this format are: 
`FECHA OPERACIÓN,CONCEPTO,IMPORTE EUR`

Function performs the following transformation of header names 
and returns pandas dataframe
```
FECHA OPERACIÓN -> Date 
CONCEPTO -> Name
[Add] Category -> "" for all 
[Add] Unit -> "EUR" for all 
IMPORTE EUR --> Amount [convert to positive]
```

Finally, remove any deposits from the record


# Dependencies
Made and tested with `Python 3.9.7`

Used Packages:
```
numpy==1.21.2
pandas==1.3.3
```
