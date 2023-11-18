import gspread
import time
from config import (PROJECT_ID, PRIVATE_KEY_ID, PRIVATE_KEY, CLIENT_EMAIL, CLIENT_ID_GOOGLE, CLIENT_CERT_URL,
                    SPREADSHEET_ID, SHEET_ID, SHEET_ID_SELLER_TRAFFIC, SHEET_ID_SELLER_ASIN)


# Google Sheets credentials
CREDS = {
  "type": "service_account",
  "project_id": PROJECT_ID,
  "private_key_id": PRIVATE_KEY_ID,
  "private_key": PRIVATE_KEY,
  "client_email": CLIENT_EMAIL,
  "client_id": CLIENT_ID_GOOGLE,
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": CLIENT_CERT_URL,
  "universe_domain": "googleapis.com"
}
SHEET_CREDENTIAL = gspread.service_account_from_dict(CREDS)

class GoogleSheet:
    def __init__(self):
        # Open the Google Sheets document
        self.spreadsheet = SHEET_CREDENTIAL.open_by_key(SPREADSHEET_ID)
        self.worksheet = self.spreadsheet.get_worksheet_by_id(SHEET_ID)

    def add_row(self, date, impressions, clicks, cost, purchases30d):
        # Add a row to the Google Sheet
        try:
            body = [date, impressions, clicks, cost, purchases30d]
            self.worksheet.append_row(body, table_range="A1")
            time.sleep(1)
        except gspread.exceptions.APIError as e:
            print(f"Error adding row to Google Sheet: {e}")

    def add_row_seller_traffic(self, date_report,	units_ordered,	total_order_items,	units_refunded,
                               ordered_product_sales_amount,	shipped_product_sales_amount,	browser_page_views,
                               browser_sessions,	mobile_app_page_views,	mobile_app_sessions):
        # Add a row to the Seller Traffic Google Sheet
        try:
            worksheet_seller = self.spreadsheet.get_worksheet_by_id(SHEET_ID_SELLER_TRAFFIC)
            body = [date_report, units_ordered, total_order_items, units_refunded, ordered_product_sales_amount,
                    shipped_product_sales_amount, browser_page_views, browser_sessions, mobile_app_page_views,
                    mobile_app_sessions]
            worksheet_seller.append_row(body, table_range="A1")
            time.sleep(1)
        except gspread.exceptions.APIError as e:
            print(f"Error adding row to Seller Traffic Google Sheet: {e}")

    def add_row_seller_asin(self,date_report, parent_asin, child_asin, total_order_items_asin, units_ordered_asin,
                            browser_page_views_asin, browser_sessions_asin, mobile_app_page_views_asin,
                            mobile_app_sessions_asin):
        # Add a row to the Seller ASIN Google Sheet
        try:
            worksheet_seller = self.spreadsheet.get_worksheet_by_id(SHEET_ID_SELLER_ASIN)
            body = [date_report, parent_asin, child_asin, total_order_items_asin, units_ordered_asin,
                    browser_page_views_asin, browser_sessions_asin, mobile_app_page_views_asin,
                    mobile_app_sessions_asin]
            worksheet_seller.append_row(body, table_range="A1")
            time.sleep(1)
        except gspread.exceptions.APIError as e:
            print(f"Error adding row to Seller ASIN Google Sheet: {e}")

    def delete_row(self, date):
        while True:
            # Find and delete a row based on the date
            cell = self.worksheet.find(date)
            if cell:
                self.worksheet.delete_rows(cell.row)
                time.sleep(1)
            else:
                break


