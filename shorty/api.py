from flask import Blueprint, request
from general.http import BadRequestResponse
from .shorteners import get_bitly_url, get_tinyurl_url

api = Blueprint('api', __name__)

@api.route('/shortlinks', methods=['POST'])
def create_shortlink():
    data: dict = request.json
    url = data.get("url")
    provider = data.get("provider") or "bitly"
    
    if not url or not isinstance(url, str):
        return BadRequestResponse("parameter url must be provided and as a string")
    
    if not provider == "bitly" and not provider == "tinyurl" or not isinstance(provider, str):
        return BadRequestResponse("provider must be 'bitly' or 'tinyurl'")
    
    return get_bitly_url(url) if provider == "bitly" else get_tinyurl_url(url)
