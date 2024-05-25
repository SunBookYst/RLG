from flask import Blueprint, request, jsonify, session
from ..services.main_service import handle_main_request
import uuid

bp = Blueprint('main', __name__, url_prefix='/main')

@bp.route('/', methods=['POST'])
def main():
    data = request.json
    user_id=session.get('user_id')
    if not user_id:
        user_id = str(uuid.uuid4())
        session['user_id'] = user_id
    response = handle_main_request(data,user_id)
    return jsonify(response)
