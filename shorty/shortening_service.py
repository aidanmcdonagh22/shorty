from typing import Dict, Tuple
from requests import post, get, Response as RequestsResponse

# These would be seperated into a .env file
BITLY_API_TOKEN = "NOTAREALTOKEN"
GROUP_GUID = "group_guid"

class ShorteningService():
    def __init__(self, url: str):
        self.url = url

    ''' Method to get Bitly Url - https://dev.bitly.com/ '''
    def get_bitly_url(self) -> Tuple[Dict[str, str], int]:
        resp: RequestsResponse = post(
            url="https://api-ssl.bitly.com/v4/shorten",
            data={
                "long_url": self.url,
                "domain": "bit.ly",
                "group_guid": GROUP_GUID
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {BITLY_API_TOKEN}"
            }
        )

        data = resp.json()

        if resp.status_code != 200 and resp.status_code != 201:
            return { "error": data["message"] }, resp.status_code

        return { "url": self.url, "link": data["link"] }, resp.status_code

    ''' Method to get Tinyurl Url - https://gist.github.com/MikeRogers0/2907534 '''
    def get_tinyurl_url(self) -> Tuple[Dict[str, str], int]:
        resp: RequestsResponse = get(f'http://tinyurl.com/api-create.php?url={self.url}')

        if resp.status_code != 200 and resp.status_code != 201:
            return { "error": "error creating tinyurl link" }, resp.status_code

        return { "url": self.url, "link": resp.text }, resp.status_code
    
    
    def attempt_to_get_bitly(self):
        bitly_attempts = 0
        
        while bitly_attempts < 3:
            data, status = self.get_bitly_url()
            if status < 200 or status > 299:
                return data, status
            else:
                bitly_attempts += 1
        
        raise Exception("too many attempts made!")

    def attempt_to_get_bitly(self):
        tinyurl_attempts = 0
        
        while tinyurl_attempts < 3:
            data, status = self.get_tinyurl_url()
            if status < 200 or status > 299:
                return data, status
            else:
                tinyurl_attempts += 1
        
        raise Exception("too many attempts made!")