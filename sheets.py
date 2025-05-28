import os
import json
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://www.googleapis.com/auth/spreadsheets"]
service_account_info = json.loads(os.environ["GCP_SERVICE_ACCOUNT"])

creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)

contact_sheet = client.open_by_key("1TgXXMH5jTETg7TgOIf8rRDpG-n1fYc57kQiaa3kMBPQ").sheet1
user_status_sheet = client.open_by_key("1oXUpo5hpru_3dKNKqNtSxMJcGln_juKKAooO2jyCatU").sheet1

# values_list = sheet.row_values(1)
# print(values_list)

def add_contact(data: dict):
    
    row = [
        data.get("Date/Time", ""),
        data.get("Name", ""),
        data.get("Phone Number", ""),
        data.get("Email", ""),
        data.get("Linkedin Profile", "")
    ]
    contact_sheet.append_row(row, value_input_option="USER_ENTERED")

def add_user_input_status(data: dict):  # stores input/status only
    row = [
        data.get("Date/Time", ""),
        data.get("User Input", ""),
        data.get("Status", "")
    ]
    user_status_sheet.append_row(row, value_input_option="USER_ENTERED")