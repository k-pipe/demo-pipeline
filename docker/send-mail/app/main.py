import argparse
import pandas as pd
import smtplib
from email.message import EmailMessage
import json
import os


def main(config_path: str, input_path: str):
    # read configuration
    with open(config_path) as f:
        config = json.load(f)
    sender_email = config["senderEmail"]
    smtp_server =  config["smtpServer"]
    smtp_port = config["smtpPort"]
    subject = config["mailSubject"]
    to = config["recipientEmail"]

    # the password is stored in K8s secret and obtained as environment variable
    email_password = os.getenv("EMAIL_PASSWORD")

    # load data from file
    print(f"Loading input data frame from file {input_path}")
    df = pd.read_json(path_or_buf=input_path, orient='records', lines=True)

    """
    Sends an email with the report for each team.
    """
    content = f"""
    <!DOCTYPE html>
    <html lang="en">
        <head>
        </head>
        <body>
            {df.to_html()}
        </body>
    </html>
    """

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(sender_email, email_password)
        email_msg = EmailMessage()
        email_msg['From'] = sender_email
        email_msg.set_content(content, subtype='html')
        email_msg['Subject'] = subject
        email_msg['To'] = to
        smtp.send_message(email_msg)

    print(f"Mail '{subject}' was sent to : {to}")
    print(f"Done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--input", required=True)
    args = vars(parser.parse_args())
    main(
        config_path=args["config"],
        input_path=args["input"],
    )
