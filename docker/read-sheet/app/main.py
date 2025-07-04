import pandas as pd
import requests
import io
import argparse
import json


def main(config_path: str, output_path: str):
    # read configuration
    with open(config_path) as f:
        config = json.load(f)
    workbook_id = config["workbookId"]
    sheet = config["sheet"]

    # read sheet from workbook into dataframe, you need to publish your sheet, in order to be able to read it without authentication:
    # in Google sheet web UI select "File" -> "Share" -> "Share with others" -> "Anyone with the link" -> "Viewer"
    print(f"Reading sheet #{sheet} of workbook {workbook_id}")
    url = f'https://docs.google.com/spreadsheets/d/{workbook_id}/export?format=csv&gid={sheet}'
    response = requests.get(url)
    df = pd.read_csv(io.StringIO(response.text))
    print(f"Read {len(df)} rows")

    # write to file in json line format
    print(f"Storing data to file {output_path}")
    df.to_json(path_or_buf=output_path, orient='records', lines=True)
    print(f"Done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    args = vars(parser.parse_args())
    main(
        config_path=args["config"],
        output_path=args["output"]
    )
