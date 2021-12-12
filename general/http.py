from flask.wrappers import Response
from flask_api import status

def BadRequestResponse(error_msg: str) -> Response:
    return { "error": error_msg }, status.HTTP_400_BAD_REQUEST