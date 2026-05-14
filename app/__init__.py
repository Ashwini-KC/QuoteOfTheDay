"""
Copywrite EDUBEX, 2025
Author: ASHWINI
CreatedDate: 14 May 2026
LastModifiedDate: 14 May 2026
"""

from flask import Flask
from config import get_config
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def create_app():
    """Application factory function"""
    config = get_config()
    app = Flask(__name__)
    app.config.from_object(config)
    
    logger.info(f"Creating Flask app with config: {config.__name__}")
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    
    # Register error handlers
    register_error_handlers(app)
    
    logger.info("Flask app created successfully")
    return app


def register_error_handlers(app):
    """Register error handlers for the application"""
    from flask import render_template, jsonify
    from app.utils.logger import setup_logger
    
    error_logger = setup_logger("error_handler")
    
    @app.errorhandler(404)
    def handle_404(error):
        error_logger.warning(f"404 Error: {error}")
        return render_template("errors/404.html"), 404
    
    @app.errorhandler(405)
    def handle_405(error):
        error_logger.warning(f"405 Error: {error}")
        return jsonify({"error": "Method not allowed"}), 405
    
    @app.errorhandler(500)
    def handle_500(error):
        error_logger.error(f"500 Error: {error}", exc_info=True)
        return render_template("errors/500.html"), 500
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        error_logger.error(f"Unexpected error: {error}", exc_info=True)
        return render_template("errors/500.html"), 500


# Dummy db object for potential future expansion
class DummyDB:
    pass

db = DummyDB()
