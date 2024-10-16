#!/usr/bin/python3
"""Create a flask application for the API"""

from flask import Blueprint


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


def check_auth_header(cls=None):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'message': 'Missing Authorization Header'}), 401
    
    parts = auth_header.split(" ")
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return jsonify({'message': 'Invalid Authorization Header'}), 401
    
    from models.depot_detail import AdminSession
    from models.candidate_session import CandidateSession

    admin_sess = storage.get(AdminSession, parts[1])
    can_sess = storage.get(CandidateSession, parts[1])
    if (((cls and cls == "AdminSession") or (not cls)) and admin_sess):
        if (admin_sess.expired()):
            return jsonify({'error': 'Session expired'}), 401
    elif (((cls and cls == "CandidateSession") or (not cls)) and can_sess):
        if (can_sess.expired()):
            return jsonify({'error': 'Session expired'}), 401
    else:
        return jsonify({'error': 'Unknown session'}), 401
    return None


from api.v1.views.index import *
from api.v1.views.operations import *
from api.v1.views.depot_details import *
