import argparse
import pandas as pd
from subprocess import run


def convert_to_csv(filename: str) -> str:

    # create new filename by taking the whole filename 
    # except for the extension and changing the extension 
    # to csv
    new_filename = filename.split('.')[:-1] + [".csv"]
    new_filename = "".join(new_filename)

    # use subprocess to convert file
    run(f"ssconvert {filename} {new_filename}")
    
    # return new file name
    return new_filename

def parse_santader_es(filename: str) -> pd.DataFrame:
    """
    Reads statement from the Spanish version of the Santander web 
    page exported as "Exportar Excel"

    Output columns of this format are: 
    FECHA OPERACIÓN,CONCEPTO,IMPORTE EUR

    Function performs the following transformation of header names 
    and returns pandas dataframe
    FECHA OPERACIÓN -> Date 
    CONCEPTO -> Name
    [Add] Category -> "" for all 
    [Add] Unit -> "Euro" for all 
    IMPORTE EUR --> Amount [Convert to positive}

    Finally, remove any deposits from the record
    """
    if ".csv" not in filename:
        filename = convert_to_csv(filename)

    # 7 lines until the headers of the table in this
    # file type
    df = pd.read_csv(filename, header=7)

    print("printing df")
    print(df)

    df.rename(columns={
            "FECHA OPERACIÓN": "Date",
            "CONCEPTO": "Name",
            "IMPORTE EUR": "Amount",
        },
        inplace = True,
        )

    # change the amount to charges
    df["Amount"] *= -1

    # filters out payments
    df = df[df["Amount"] > 0]

    # makes blank "Category"
    df["Category"] = ""

    # Makes "Unit" column
    df["Unit"] = "EUR"

    # reoder columns
    df = df[["Date", "Name", "Category", "Amount", "Unit"]]

    return df


def parse_bofa(filename: str) -> pd.DataFrame:
    """
    Reads statement from the Bank of America web page exported as 
    "Microsoft Excel Format" (csv)

    Output columns of this format are: 
    Posted Date,Reference Number,Payee,Address,Amount

    Function performs the following transformation of header names 
    and returns pandas dataframe
    Posted Date -> Date (keep the same)
    Reference Number -> [Delete]
    Payee -> Name
    Address -> [Delete]
    [Add] Category -> "" for all 
    [Add] Unit -> "USD" for all 
    Amount -> [Same]

    Finally, any Entries that say "PAYMENT - THANK YOU"
    """

    df = pd.read_csv(filename)

    df.drop(["Address", "Reference Number"], inplace=True, axis=1)
    df.rename(columns={
            "Posted Date": "Date",
            "Payee": "Name",
        },
        inplace = True,
        )

    # change the amount to charges
    df["Amount"] *= -1

    # filters out payments
    df = df[df["Amount"] > 0]

    # makes blank "Category"
    df["Category"] = ""

    # Makes "Unit" column
    df["Unit"] = "USD"

    # reoder columns
    df = df[["Date", "Name", "Category", "Amount", "Unit"]]

    return df


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-file", "-f",
            required=True,
            type=str,
            help="location of the input file",
                    )

    parser.add_argument("-output", "-o",
            type=str,
            default="out.csv",
            help="location of the output file",
                    )

    parser.add_argument("-type", "-t",
            choices = ["bofa", "santander"],
            type = str,
            default= "bofa",
            help= "type of bankstatement"
            )

    args = parser.parse_args()
    print(args)

    if args.type == "bofa":
        output = parse_bofa(args.file)
    elif args.type == "santander":
        output = parse_santader_es(args.file)
    else:
        output = pd.DataFrame()

    output.to_csv(args.output)

    print(f"successfully written to ouput file {args.output}")




if __name__ == "__main__":
    main()





