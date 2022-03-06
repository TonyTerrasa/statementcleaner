# statementcleaner
Small Python script that helps me clean csv downloads from my bank to the format I use for my budget spreadsheet

The two banks I'm currently using and Bank of America and Santander (Spain). This script takes in the a csv exported from either of these two banks and transforms it into a format which is conveient for my own personal purchase log in my budget

# Usage
```
usage: cleaner.py [-h] -f FILE [-o OUTPUT] [-b] [-s] [-p]

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  location of the input file
  -o OUTPUT, --output OUTPUT
                        location of the output file
  -b, --bofa            bankstatement is type bank of america
  -s, --santander       bankstatement is type Santander
  -p, --purchase-log    bankstatement is type from purchase log format
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


## Purchase Log 
Reads the purchase log format that I use. It has the following column transformations
```
Date -> Date 
Amount -> Amount 
Source -> [Delete]
[Add] Category -> "" for all 
[Add] Unit -> "EUR" for all 
Description -> Name
```

# Dependencies
Made and tested with `Python 3.9.7`

Used Packages:
```
numpy==1.21.2
pandas==1.3.3
```
