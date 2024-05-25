from flask import Blueprint, request, jsonify
from ..services.other_service import handle_others_request

bp = Blueprint('others', __name__, url_prefix='/others')

@bp.route('/', methods=['POST'])
def others():
    data = request.json
    response = handle_others_request(data)
    return jsonify(response)
