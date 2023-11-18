import requests
import os

# Amazon Seller API credentials
REFRESH_TOKEN_SELLER = os.environ.get('refresh_token_seller')
CLIENT_SELLER_ID = os.environ.get('client_seller_id')
CLIENT_SELLER_SECRET = os.environ.get('client_seller_secret')


class AccessTokenSeller:
    def __init__(self):
        self.headers = {
                    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                }

    def get_access_token(self):
        # Set data for the access token request
        data = {
                    'grant_type': 'refresh_token',
                    'client_id': CLIENT_SELLER_ID,
                    'refresh_token': REFRESH_TOKEN_SELLER,
                    'client_secret': CLIENT_SELLER_SECRET
                }

        # Send a POST request to get the access token
        try:
            response = requests.post('https://api.amazon.com/auth/o2/token', data=data, headers=self.headers)
            response.raise_for_status()
            return response.json()['access_token']
        except requests.exceptions.RequestException as e:
            print(f"Error getting Seller access token: {e}")
            return None