from flask import Blueprint, request, jsonify
from ..services.bag_service import handle_bag_request

bp = Blueprint('bag', __name__, url_prefix='/bag')

@bp.route('/', methods=['POST'])
def bag():
    data = request.json
    response = handle_bag_request(data)
    return jsonify(response)
