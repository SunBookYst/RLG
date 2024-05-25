from flask import Blueprint, request, jsonify
from ..services.time_service import handle_time_request

bp = Blueprint('time', __name__, url_prefix='/time')

@bp.route('/', methods=['POST'])
def time():
    data = request.json
    response = handle_time_request(data)
    return jsonify(response)
