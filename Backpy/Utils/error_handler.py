from Flask import jsonify

def setup_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Page not found"}),404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad request"}), 400


    
