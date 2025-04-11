import os.path
import os
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
load_dotenv()  # This loads the variables from .env

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
RANGE_NAME = os.getenv("RANGE_NAME")

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # If there are no (valid) credentials available, let the user log in.


def append_values( values):
    """Appends values to a sample spreadsheet."""
    creds = None
    if os.path.exists("credentials.json"):
        creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = Credentials.from_service_account_file(
                "credentials.json", scopes=SCOPES
            )

    try:
        service = build("sheets", "v4", credentials=creds)
        body = {"values": values}
        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE_NAME,
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )

        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


def main():
    values = [
        [
            "95141502",
            "سعید خدام",
            "2000-12-06",
            "مجرد",
            "خیر",
            "خیر",
            "کامپیوتر",
            "1",
            "لیسانس",
            "خیر",
            "خیر",
            "خیر",
            "خیر",
            "هیچ",
            "هیچ",
            "7",
            "خیر",
        ]
    ]
    append_values(values)


if __name__ == "__main__":
    main()
