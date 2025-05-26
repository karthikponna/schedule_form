import os
import json
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://www.googleapis.com/auth/spreadsheets"]
service_account_info = json.loads(os.environ["GCP_SERVICE_ACCOUNT"])

creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)

sheet = client.open_by_key("1TgXXMH5jTETg7TgOIf8rRDpG-n1fYc57kQiaa3kMBPQ").sheet1

# values_list = sheet.row_values(1)
# print(values_list)

def add_contact(data: dict):
    
    row = [
        datetime.datetime.utcnow().isoformat(),
        data["name"],
        data["phone"],
        data["email"],
        data["linkedin"]
    ]
    sheet.append_row(row, value_input_option="USER_ENTERED")
