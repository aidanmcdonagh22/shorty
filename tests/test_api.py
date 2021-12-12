from .utils import check_api_response
from requests_mock import Mocker

# Integration Testing
class TestShortlinkView:
    def test_no_url(self, client):
        # perform client post to endpoint
        response = client.post('/shortlinks', json={ "provider": "bitly" })
        
        # check response
        check_api_response(response, 400, { "error": "parameter url must be provided and as a string" })

    def test_bad_provider(self, client):
        # perform client post to endpoint
        response = client.post('/shortlinks', json={
            "url": "https://google.com", "provider": "somethingrandom"
        })
        
        # check response
        check_api_response(response, 400, { "error": "provider must be 'bitly' or 'tinyurl'" })

    def test_successful_response_bitly(self, client):
        url = "https://google.com"
        shortlink = "http://short.com"
        with Mocker() as m:
            # mock response
            m.post("https://api-ssl.bitly.com/v4/shorten", json={ "link": shortlink })
            
            # perform client post to endpoint
            response = client.post('/shortlinks', json={
                "url": url, "provider": "bitly"
            })
            
            # check response
            check_api_response(response, 200, { "url": url, "link": shortlink })

    def test_unsuccessful_response_bitly(self, client):
        url = "https://google.com"
        errorMsg = "Error: we could not provide you a link"
        
        with Mocker() as m:
            # mock response
            m.post("https://api-ssl.bitly.com/v4/shorten", json={ "message": errorMsg }, status_code=400)
            
            # perform client post to endpoint
            response = client.post('/shortlinks', json={
                "url": url, "provider": "bitly"
            })
            
            # check response
            check_api_response(response, 400, { "error": errorMsg })

    def test_successful_response_tinyurl(self, client):
        url = "https://facebook.com"
        shortlink = "http://short.com"
        with Mocker() as m:
            # mock response
            m.get(f"http://tinyurl.com/api-create.php?url={url}", text=shortlink)
            
            # perform client post to endpoint
            response = client.post('/shortlinks', json={
                "url": url, "provider": "tinyurl"
            })
        
            # check response
            check_api_response(response, 200, { "url": url, "link": shortlink })

    def test_unsuccessful_response_tinyurl(self, client):
        url = "https://facebook.com"
        error = "error creating tinyurl link"
        
        with Mocker() as m:
            # mock response
            m.get(f"http://tinyurl.com/api-create.php?url={url}", text=error, status_code=400)
            
            # perform client post to endpoint
            response = client.post('/shortlinks', json={
                "url": url, "provider": "tinyurl"
            })
        
            # check response
            check_api_response(response, 400, { "error": error })
