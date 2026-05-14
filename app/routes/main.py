"""
Copywrite ASHWINI, 2026
Author: ASHWINI
CreatedDate: 14 May 2026
LastModifiedDate: 14 May 2026
"""

from flask import Blueprint, render_template, current_app
from app.services.quote_service import QuoteService
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
def index():
    """Homepage route - display quote of the day"""
    try:
        quote = QuoteService.get_quote_of_the_day(current_app.config["QUOTES_FILE"])
        logger.info("Homepage accessed successfully")
        return render_template("index.html", quote=quote)
    except Exception as e:
        logger.error(f"Error in index route: {e}")
        return render_template("errors/500.html"), 500


@main_bp.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    logger.info("Health check requested")
    return {"status": "healthy"}, 200
