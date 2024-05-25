from flask import Blueprint, request, jsonify
from ..services.status_service import handle_status_request

bp = Blueprint('status', __name__, url_prefix='/status')

@bp.route('/', methods=['POST'])
def status():
    data = request.json
    response = handle_status_request(data)
    return jsonify(response)
