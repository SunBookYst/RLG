from flask import Blueprint, request, jsonify
from ..services.task_info_service import handle_task_info_request

bp = Blueprint('task_info', __name__, url_prefix='/task_info')

@bp.route('/', methods=['POST'])
def task_info():
    data = request.json
    response = handle_task_info_request(data)
    return jsonify(response)
