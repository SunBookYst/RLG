from flask import Blueprint, request, jsonify
from ..services.feedback_service import handle_feedback_request

bp = Blueprint('feedback', __name__, url_prefix='/feedback')

@bp.route('/', methods=['POST'])
def feedback():
    data = request.json
    response = handle_feedback_request(data)
    return jsonify(response)
