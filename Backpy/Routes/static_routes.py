from Flask import Blueprint, send_from_directory

static_bp = Blueprint('static', __name__)

@static_bp.route('/static/<path:filename>', methods=['GET'])
def serve_static(filename):
    return send_from_directory('static_files_directory', filename)
