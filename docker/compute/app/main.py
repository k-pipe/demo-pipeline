import argparse
import pandas as pd


def main(input_path: str, output_path: str):
    # load data from file
    print(f"Loading input data frame from file {input_path}")
    df = pd.read_json(path_or_buf=input_path, orient='records', lines=True)

    # compute result column
    df['difference_of_squares'] = df.apply(lambda row: row.a**2 + row.b**2 - row.c**2, axis=1)
    print(f"Processed {len(df)} rows")

    # store to output file
    print(f"Writing data to file {output_path}")
    df.to_json(path_or_buf=output_path, orient='records', lines=True)

    print(f"Done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=False)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = vars(parser.parse_args())
    main(
        input_path=args["input"],
        output_path=args["output"]
    )
