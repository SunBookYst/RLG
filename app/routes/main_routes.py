from flask import Blueprint, request, jsonify
from ..services.main_service import handle_main_request

bp = Blueprint('main', __name__, url_prefix='/main')

@bp.route('/', methods=['POST'])
def main():
    data = request.json
    response = handle_main_request(data)
    return jsonify(response)
