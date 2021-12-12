from general.http import BadRequestResponse

class TestBadRequestResponse:
    def test_response(self):
        error = "this is my error message"
        response = BadRequestResponse(error)
        
        assert response[0] == { "error": error }
        assert response[1] == 400