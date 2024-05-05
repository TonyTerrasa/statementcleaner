import argparse
import pandas as pd
import datetime


output_columns = ["Date", "Name", "Category", "Amount", "Source"]


def parse_purchase_log(filename: str) -> pd.DataFrame:
    """
    Reads statement from the the format of purchase log that I
    use on my computer. It generally follows the format:
    - DATE,AMOUNT($/€),cardoption,description

    However, it will not have any headers

    Function adds headers, and fills the appropriate columns
    and returns pandas dataframe

    [Remove the '-' character]
    col1                 -> Date
    col2                -> Amount
    [Add] Category       -> "" for all
    [Add] Source       -> "BA Checking" for all
    col4                 -> Name


    Order: Date,Name,Catagory,Amount,Unit
    """
    assert (
        ".csv" in filename
    ), "csv is the only supported file time for the purchase log"

    df = pd.read_csv(filename)

    # trim any leading or trailing spaces
    names_stripped = {col_name: col_name.strip() for col_name in df.columns}

    df.rename(columns=names_stripped, inplace=True)

    # remove the Source column
    # df.drop(["Source"], inplace=True, axis=1)

    # remove the "-" by taking out the first character or each entry
    df["Date"] = df["Date"].apply(
        lambda x: x[1:].strip() if x[0] == "-" else x.strip(), convert_dtype=True
    )

    # remove preceding or trailing spaces from the entries in Description
    df["Description"] = df["Description"].apply(lambda x: str(x).strip())
    # change the name of the Description column
    df.rename(
        columns={
            "Description": "Name",
        },
        inplace=True,
    )

    # makes blank "Category"
    df["Category"] = ""

    # Makes "Source" column
    df["Source"] = "BA Checking"

    # reoder columns and return everything except the "Source" Column
    df = df[output_columns]

    print(df)

    return df


def parse_usaa(filename: str) -> pd.DataFrame:
    """
    Reads statement from USAA web page hitting "Export"
    Output columns of this format are:
    Date,Description,Original Description,Category,Amount,Status
    Function performs the following transformation of header names
    and returns pandas dataframe

    Date -> [Same]
    Description -> Name
    Original Description -> [Delete]
    Category -> [Delete]
    Status -> [Delete]

    [Add] Category -> "" for all
    [Add] Unit -> "USD" for all
    Amount -> [Same]

    """

    df = pd.read_csv(filename)

    df.drop(["Original Description", "Category", "Status"], inplace=True, axis=1)
    df.rename(
        columns={
            "Description": "Name",
        },
        inplace=True,
    )

    # change the amount to charges
    df["Amount"] *= -1

    # filters out money put INTO the account
    # also take out transfers (not purchases)
    df = df[df["Amount"] > 0]
    df = df[df["Name"] != "USAA Transfer"]

    # makes blank "Category"
    df["Category"] = ""

    # Makes "Source" column
    df["Source"] = "USAA"

    # reoder columns
    df = df[output_columns]

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
    Finally, remove any Entries that say "PAYMENT - THANK YOU"
    """

    df = pd.read_csv(filename)

    df.drop(["Address", "Reference Number"], inplace=True, axis=1)
    df.rename(
        columns={
            "Posted Date": "Date",
            "Payee": "Name",
        },
        inplace=True,
    )

    # change the amount to charges
    df["Amount"] *= -1

    # filters out payments
    df = df[df["Amount"] > 0]

    # makes blank "Category"
    df["Category"] = ""

    # Makes "Source" column
    df["Source"] = "BofA"

    # reoder columns
    df = df[output_columns]

    return df


def detect_file_source(filename: str) -> str:
    """Checks a file to see where it came from options are:
    usaa
    bofa
    log
    unrecognized
    """

    with open(filename, "r") as file:
        first_line = file.readline().strip()

    if first_line == "Date,Description,Original Description,Category,Amount,Status":
        return "usaa"
    elif first_line == "Posted Date,Reference Number,Payee,Address,Amount":
        return "bofa"
    elif first_line == "Date,Amount,Description":
        return "log"
    else:
        return "unrecognized"


def main():
    parser = argparse.ArgumentParser(
        description="convert a set of bank statements into the same csv format"
    )

    # using nargs will allow argparse to check automatically that at lease one file has been input
    parser.add_argument("input_files", nargs="+", help="List of input files to process")
    # Output file - optional, specified with a flag
    date_string = datetime.date.today().strftime("%Y%m%d")
    parser.add_argument(
        "--output",
        help="Output file (optional)",
        default=f"purchas_log_{date_string}.csv",
    )

    args = parser.parse_args()

    # loop over input files and generate data frames from each one
    outputs = []
    for filename in args.input_files:
        file_source = detect_file_source(filename)
        if file_source == "usaa":
            outputs.append(parse_usaa(filename))
        elif file_source == "bofa":
            outputs.append(parse_bofa(filename))
        elif file_source == "log":
            outputs.append(parse_purchase_log(filename))
        else:
            raise ValueError(f"File '{filename}' is of an unrecognized log type.")

    # make the final file and output to csv
    result = pd.concat(outputs, ignore_index=True)
    result = result.sort_values(by="Date", ignore_index=True, ascending=True)
    result["Name"] = result["Name"].str.lower()
    result.to_csv(args.output, index=False)

    print(f"successfully written to ouput file {args.output}")


if __name__ == "__main__":
    main()
