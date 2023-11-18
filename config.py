import os

# Amazon Advertising API credentials
REFRESH_TOKEN = os.environ.get('refresh_token')
CLIENT_ID = os.environ.get('client_id')
CLIENT_SECRET = os.environ.get('client_secret')
PROFILE_ID = os.environ.get('profile_id')

# API URLs
URL_ACCESS_TOKEN = 'https://api.amazon.com/auth/o2/token'

# Amazon Seller API credentials
REPORT_TYPE = 'GET_SALES_AND_TRAFFIC_REPORT'
URL_REPORT_SELLER = 'https://sellingpartnerapi-na.amazon.com'
REFRESH_TOKEN_SELLER = os.environ.get('refresh_token_seller')
CLIENT_SELLER_ID = os.environ.get('client_seller_id')
CLIENT_SELLER_SECRET = os.environ.get('client_seller_secret')

# Google Sheets API credentials
SPREADSHEET_ID = os.environ.get("spreadsheet_id")
SHEET_ID = os.environ.get("sheet_id")
PROJECT_ID = os.environ.get("project_id")
SHEET_ID_SELLER_TRAFFIC = os.environ.get("sheet_id_seller_traffic")
SHEET_ID_SELLER_ASIN = os.environ.get("sheet_id_seller_asin")
PRIVATE_KEY_ID = os.environ.get("private_key_id")
PRIVATE_KEY = os.environ.get("private_key").replace(r'\n', '\n')
CLIENT_EMAIL = os.environ.get("client_email")
CLIENT_ID_GOOGLE = os.environ.get("client_id_google")
CLIENT_CERT_URL = os.environ.get("client_cert_url")