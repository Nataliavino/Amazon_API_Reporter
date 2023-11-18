import time
import json
import gzip
import requests
import os

REFRESH_TOKEN = os.environ.get('refresh_token')
CLIENT_ID = os.environ.get('client_id')
CLIENT_SECRET = os.environ.get('client_secret')
PROFILE_ID = os.environ.get('profile_id')


class Report:
    def __init__(self, token):
        self.token = token
        self.header = {
            'Amazon-Advertising-API-ClientId': CLIENT_ID,
            'Authorization': self.token,
            'Amazon-Advertising-API-Scope': PROFILE_ID,
            'Accept': 'application/vnd.sbcampaignresource.v4+json',
            'Content-Type': 'text/plain'}
        self.id = ''
        self.date_report = ''
        self.impressions = 0
        self.clicks = 0
        self.cost = 0
        self.purchases30d = 0

    def get_report_id(self,start_date,end_date):
        # Set data for the report id request
        data = {
            "startDate": start_date,
            "endDate": end_date,
            "configuration": {
                "adProduct": "SPONSORED_PRODUCTS",
                "groupBy": ["campaign"],
                "columns": ["impressions", "clicks", "cost", "date", "purchases30d"],
                "reportTypeId": "spCampaigns",
                "timeUnit": "DAILY",
                "format": "GZIP_JSON"
            }
        }

        # Send a POST request to get the report id
        try:
            response = requests.post('https://advertising-api.amazon.com/reporting/reports', headers=self.header, json=data)
            response.raise_for_status()
            self.id = response.json()['reportId']
        except requests.exceptions.RequestException as e:
            print(f"Error getting report ID: {e}")

    def get_request(self):
        # Send a GET request to get the report details
        try:
            response = requests.get(
                f'https://advertising-api.amazon.com/reporting/reports/{self.id}',
                headers=self.header)
            response.raise_for_status()
            print('Preparing a report...')
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting report request: {e}")

    def get_link_report(self):
        # Check if the report status is completed
        while True:
            if self.get_request()['status'] != 'COMPLETED':
                time.sleep(20)
            else:
                break
        # Return the report URL
        return self.get_request()['url']

    def download_report(self, link, date):
        print('Downloading report.')
        # Send a GET request to download the report
        try:
            response = requests.get(link, verify=True)
            response.raise_for_status()
            # Save the report to a file
            with open(f'reports/report-{date}.json.gz', 'wb') as f:
                file = f.write(response.content)
            return file
        except requests.exceptions.RequestException as e:
            print(f"Error downloading report: {e}")

    def read_report(self, date):
        # Read the report from the saved file
        try:
            with gzip.open(f'reports/report-{date}.json.gz') as f:
                data = f.read()
            return json.loads(data)
        except FileNotFoundError as e:
            print(f"Error reading report file: {e}")
            return None

    def iterate_report(self, data):
        # Extract relevant data from the report
        try:
            self.date_report = data['date']
            self.impressions = data['impressions']
            self.clicks = data['clicks']
            self.cost = data['cost']
            self.purchases30d = data['purchases30d']
        except KeyError as e:
            print(f"Error iterating report data: {e}")

    def delete_file(self, date):
        # Delete the saved report file
        try:
            os.remove(f'reports/report-{date}.json.gz')
        except FileNotFoundError as e:
            print(f"Error deleting report file: {e}")