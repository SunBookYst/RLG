from flask import Blueprint, request, jsonify
from ..services.accept_service import handle_accept_request

bp = Blueprint('accept', __name__, url_prefix='/accept')

@bp.route('/', methods=['POST'])
def accept():
    data = request.json
    response = handle_accept_request(data)
    return jsonify(response)
