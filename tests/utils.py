
from flask.wrappers import Response as FlaskResponse

def check_api_response(response: FlaskResponse, status_code: int, data) -> None:
    print(response.json)
    assert response.json  == data
    assert response.status_code == status_code

def check_flask_response(response: FlaskResponse, status_code: int, data) -> None:
    assert response[0]  == data
    assert response[1] == status_code