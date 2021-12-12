from typing import Dict, Tuple
from requests import post, get, Response as RequestsResponse

# These would be seperated into a .env file
BITLY_API_TOKEN = "NOTAREALTOKEN"
GROUP_GUID = "group_guid"

''' Method to get Bitly Url - https://dev.bitly.com/ '''
def get_bitly_url(url: str) -> Tuple[Dict[str, str], int]:
    resp: RequestsResponse = post(
        url="https://api-ssl.bitly.com/v4/shorten",
        data={
            "long_url": url,
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

    return { "url": url, "link": data["link"] }, resp.status_code

''' Method to get Tinyurl Url - https://gist.github.com/MikeRogers0/2907534 '''
def get_tinyurl_url(url: str) -> Tuple[Dict[str, str], int]:
    resp: RequestsResponse = get(f'http://tinyurl.com/api-create.php?url={url}')

    if resp.status_code != 200 and resp.status_code != 201:
        return { "error": "error creating tinyurl link" }, resp.status_code

    return { "url": url, "link": resp.text }, resp.status_code