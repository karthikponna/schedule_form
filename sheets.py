import os
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://www.googleapis.com/auth/spreadsheets"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open_by_key("1TgXXMH5jTETg7TgOIf8rRDpG-n1fYc57kQiaa3kMBPQ").sheet1

# values_list = sheet.row_values(1)
# print(values_list)

def add_contact(data: dict):
    # append a timestamp + all fields
    row = [
        datetime.datetime.utcnow().isoformat(),
        data["name"],
        data["phone"],
        data["email"],
        data["linkedin"]
    ]
    sheet.append_row(row, value_input_option="USER_ENTERED")
