import requests
#Basic
class SafeW:
    def __init__(self, token: str):
        self.token = token
        self.base_url = f"https://api.safew.org/bot{token}/"

    def request(self, method: str, data=None, files=None):
        url = self.base_url + method
        response = requests.post(url, data=data, files=files)
        try:
            res = response.json()
            if not res.get("ok", False):
                raise Exception(res)
            return res
        except Exception as e:
            raise Exception(f"Request failed: {e}")