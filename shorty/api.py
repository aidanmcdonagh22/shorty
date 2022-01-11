from flask import Blueprint, request
from general.http import BadRequestResponse
from .shortening_service import ShorteningService

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
    
    shortening_service: ShorteningService = ShorteningService(url)
    
    if provider == "bitly":
        try:
            return shortening_service.attempt_to_get_bitly()
        except:
            return shortening_service.attempt_to_get_tinyurl()
    else:
        try:
            return shortening_service.attempt_to_get_tinyurl()
        except:
            return shortening_service.attempt_to_get_bitly()
