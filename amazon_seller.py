import datetime
import time
import json
import gzip
import requests
import os

REPORT_TYPE = 'GET_SALES_AND_TRAFFIC_REPORT'
URL = 'https://sellingpartnerapi-na.amazon.com'
REFRESH_TOKEN_SELLER = os.environ.get('refresh_token_seller')


class ReportSeller:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'content-type': 'application/json',
            'Accept': 'application/json',
            'x-amz-access-token': self.token,
        }
        self.id = ''
        self.document_id = ''
        self.date = str(datetime.datetime.now() - datetime.timedelta(days=2))[:10]
        self.date_report = ''
        self.units_ordered = 0
        self.total_order_items = 0
        self.units_refunded = 0
        self.ordered_product_sales_amount = 0
        self.shipped_product_sales_amount = 0
        self.browser_page_views = 0
        self.browser_sessions = 0
        self.mobile_app_page_views = 0
        self.mobile_app_sessions = 0
        self.date_by_asin_report = ''
        self.parent_asin = ''
        self.child_asin = ''
        self.total_order_items_asin = 0
        self.units_ordered_asin = 0
        self.browser_page_views_asin = 0
        self.browser_sessions_asin = 0

    def get_report_id(self):
        # Set parameters for the report id request
        param = {
                'marketplaceIds': ['ATVPDKIKX0DER'],
                'reportType': REPORT_TYPE,
                'reportOptions': {'dateGranularity': 'DAY', 'asinGranularity': 'CHILD'},
                'dataStartTime': self.date,
                'dataEndTime': self.date
        }

        # Send a POST request to get the report id
        try:
            response = requests.post(f'{URL}/reports/2021-06-30/reports', json=param,headers=self.headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            self.id = response.json()['reportId']
        except requests.exceptions.RequestException as e:
            print(f"Error getting report ID: {e}")

    def get_report_document_id(self):
        # Send a GET request to get the report document id
        try:
            response = requests.get(f'{URL}/reports/2021-06-30/reports/{self.id}', headers=self.headers)
            response.raise_for_status()
            print('Waiting document id...')
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting Seller report document ID: {e}")

    def get_link_report_document_id(self):
        while True:
            # Check if the report document id is done processing
            if self.get_report_document_id()['processingStatus'] != 'DONE':
                time.sleep(10)
            else:
                self.document_id = self.get_report_document_id()['reportDocumentId']
                break
        return self.get_report_document_id()

    def get_report_by_document_id(self):
        # Send a GET request to get the report by document id
        try:
            response = requests.get(f'{URL}/reports/2021-06-30/documents/{self.document_id}', headers=self.headers)
            response.raise_for_status()
            return response.json()['url']
        except requests.exceptions.RequestException as e:
            print(f"Error getting Seller report by document ID: {e}")

    def download_report(self, link, date, save_directory='report_seller'):
        print('Downloading report.')
        # Specify the file path
        file_path = os.path.join(save_directory, f'report-{date}.json.gz')

        try:
            response = requests.get(link, verify=True)
            response.raise_for_status()
            # Save the report to the specified file path
            with open(file_path, 'wb') as f:
                file = f.write(response.content)
            return file
        except requests.exceptions.RequestException as e:
            print(f"Error downloading report: {e}")

    def read_report(self):
        # Read the report from the saved file
        try:
            with gzip.open(f'report_seller/report-{self.date}.json.gz') as f:
                data = f.read()
            return json.loads(data)
        except FileNotFoundError as e:
            print(f"Error reading Seller report file: {e}")
            return None

    def iterate_report_by_day(self, data):
        # Extract relevant data from the report for daily metrics
        try:
            self.date_report = data['date']
            self.units_ordered = data['salesByDate']['unitsOrdered']
            self.total_order_items = data['salesByDate']['totalOrderItems']
            self.units_refunded = data['salesByDate']['unitsRefunded']
            self.ordered_product_sales_amount = data['salesByDate']['orderedProductSales']['amount']
            self.shipped_product_sales_amount = data['salesByDate']['shippedProductSales']['amount']
            self.browser_page_views = data['trafficByDate']['browserPageViews']
            self.browser_sessions = data['trafficByDate']['browserSessions']
            self.mobile_app_page_views = data['trafficByDate']['mobileAppPageViews']
            self.mobile_app_sessions = data['trafficByDate']['mobileAppSessions']
        except KeyError as e:
            print(f"Error iterating Seller report by day: {e}")

    def iterate_report_by_asin(self, data):
        # Extract relevant data from the report for ASIN metrics
        try:
            self.parent_asin = data['parentAsin']
            self.child_asin = data['childAsin']
            self.total_order_items_asin = data['salesByAsin']['totalOrderItems']
            self.units_ordered_asin = data['salesByAsin']['unitsOrdered']
            self.browser_page_views_asin = data['trafficByAsin']['browserPageViews']
            self.browser_sessions_asin = data['trafficByAsin']['browserSessions']
        except KeyError as e:
            print(f"Error iterating Seller report by ASIN: {e}")

    def delete_file(self, date, save_directory='report_seller'):
        # Specify the file path for deletion
        file_path = os.path.join(save_directory, f'report-{date}.json.gz')

        # Delete the saved report file
        try:
            os.remove(file_path)
        except FileNotFoundError as e:
            print(f"File Amazon Seller not found. Error deleting report file: {e}")