import requests

class GerritAPIManager:
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip('/')
        self.auth = (username, password)

    def get_response(self):

        url = f"{self.base_url}"
        print(url)
        response = requests.get(url, auth=self.auth)
        if response.status_code == 200:

            print(response.text)
        else:
            print(f"Failed to fetch changes: {response.status_code}")
            return None
