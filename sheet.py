import os.path
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.cloud import secretmanager
from google.auth.transport.requests import Request
import json

# Create a Secret Manager client
client = secretmanager.SecretManagerServiceClient()

SPREADSHEET_ID = "SPREADSHEET_ID"
RANGE_NAME = "RANGE_NAME"
CREDENTIALS = "credentials"
project_id = "70217429413" # You'll need to put your project ID here
SPREADSHEET_ID_SECRET_NAME = f"projects/{project_id}/secrets/{SPREADSHEET_ID}/versions/latest"
RANGE_NAME_SECRET_NAME = f"projects/{project_id}/secrets/{RANGE_NAME}/versions/latest"
CREDENTIALS_SECRET_NAME = f"projects/{project_id}/secrets/{CREDENTIALS}/versions/latest"


try:
    # Get the latest version of the secret
    response = client.access_secret_version(name=SPREADSHEET_ID_SECRET_NAME)

    # The secret data is in the 'payload'
    spreadsheet_id = response.payload.data.decode("utf-8")
    # Now you can use the api_key in your program!
    print(f"Your spreadsheet_id is: {spreadsheet_id}")

except Exception as e:
    print(f"Something went wrong: {e}")
try:
    # Get the latest version of the secret
    response = client.access_secret_version(name=SPREADSHEET_ID_SECRET_NAME)

    # The secret data is in the 'payload'
    range_name = response.payload.data.decode("utf-8")
    # Now you can use the api_key in your program!
    print(f"Your range_name is: {range_name}")

except Exception as e:
    print(f"Something went wrong: {e}")
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # If there are no (valid) credentials available, let the user log in.



try:
    response = client.access_secret_version(name=CREDENTIALS_SECRET_NAME)
    credentials_json = response.payload.data.decode("utf-8")
    credentials_info = json.loads(credentials_json)
    creds = service_account.Credentials.from_service_account_info(credentials_info, scopes=SCOPES)
    print(f"your credentials ={creds}")
    
except Exception as e:
    print(f"An error occurred while accessing the secret: {e}")
    

def append_values(values):
    """Appends values to a sample spreadsheet using credentials from Secret Manager."""

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # You might need to import Request from google.auth.transport.requests
        else:
            print("Error: Could not retrieve valid credentials from Secret Manager.")
            return None

    try:
        service = build("sheets", "v4", credentials=creds)
        body = {"values": values}
        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
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
