from flask import Flask
from services.database_service import init_db
from routes.user_routes import user_bp
from routes.static_routes import static_bp
from utils.error_handler import setup_error_handlers

def create_app():
    app = Flask(_name_)

    app.config.from_json('confing.json')

    init_db(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(static_bp)

    setup_error_handlers(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=8080, debug=True)

    
