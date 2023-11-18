import requests
import os


# Amazon API credentials from environment variables
CLIENT_ID = os.environ.get('client_id')
CLIENT_SECRET = os.environ.get('client_secret')
URL = 'https://api.amazon.com/auth/o2/token'


class AccessToken:
    def __init__(self, token):
        self.token = token

    def get_access_token(self):
        # Set headers for the access token request
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        }

        # Set data for the access token request
        data = {
            'grant_type': 'refresh_token',
            'client_id': CLIENT_ID,
            'refresh_token': self.token,
            'client_secret': CLIENT_SECRET
        }

        # Send a POST request to get the access token
        try:
            response = requests.post(URL, headers=headers, data=data)
            response.raise_for_status()
            r_json = response.json()
            return r_json["access_token"]
        except requests.exceptions.RequestException as e:
            print(f"Error getting access token: {e}")