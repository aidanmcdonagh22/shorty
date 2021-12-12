from shorty.shorteners import get_bitly_url, get_tinyurl_url
import responses
from .utils import check_flask_response

# unit testing
class TestBitlyURLShortener:

    @responses.activate
    def test_successful_response(self):
        inputURL = "https://google.com"
        outputURL = "https://testbitlyone.com"
        endpoint = "https://api-ssl.bitly.com/v4/shorten"
        
        responses.add('POST', url=endpoint, json={ "link": outputURL }, status=200)
        
        response = get_bitly_url(inputURL)
        
        # check requests call
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "POST"
        assert responses.calls[0].request.url == endpoint
        
        # check flask response
        check_flask_response(response, 200, {
            "url": inputURL,
            "link": outputURL
        })

    @responses.activate
    def test_unsuccessful_response(self):
        inputURL = "https://google.com"
        endpoint = "https://api-ssl.bitly.com/v4/shorten"
        errorMsg = "Error: we could not provide you a link"
        
        responses.add('POST', url=endpoint, json={ "message": errorMsg }, status=400)
        
        response = get_bitly_url(inputURL)
        
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "POST"
        assert responses.calls[0].request.url == endpoint
        
        check_flask_response(response, 400, { "error": errorMsg })

class TestTinyURLShortener:
    
    @responses.activate
    def test_successful_response(self):
        inputURL = "https://testtiny.com"
        endpoint = f"http://tinyurl.com/api-create.php?url={inputURL}"
        outputURL = "https://madeuplink.com"
        
        responses.add('GET', url=endpoint, body=outputURL, status=200)
        
        response = get_tinyurl_url(inputURL)
        
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == endpoint
        
        check_flask_response(response, 200, {
            "url": inputURL, "link": outputURL
        })

    @responses.activate
    def test_unsuccessful_response(self):
        inputURL = "https://testtiny.com"
        endpoint = f"http://tinyurl.com/api-create.php?url={inputURL}"
        error = "error creating tinyurl link"
        
        responses.add('GET', url=endpoint, body=error, status=400)
        
        response = get_tinyurl_url(inputURL)
        
        assert len(responses.calls) == 1
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == endpoint
        
        check_flask_response(response, 400, { "error": error })