import argparse
from typing import List
import pandas as pd
from pandas.core.frame import DataFrame

def parse_santader(filename: str) -> pd.DataFrame:
    return pd.DataFrame()

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

    if args.type == "bofa":
        output = parse_bofa(args.file)
    elif args.type == "santader":
        output = parse_bofa(args.file)
    else:
        output = pd.DataFrame()

    output.to_csv(args.output)

    print(f"successfully written to ouput file {args.output}")




if __name__ == "__main__":
    main()





