from flask import Blueprint, request, jsonify
from ..services.skill_service import handle_skill_request

bp = Blueprint('skill', __name__, url_prefix='/skill')

@bp.route('/', methods=['POST'])
def skill():
    data = request.json
    response = handle_skill_request(data)
    return jsonify(response)
