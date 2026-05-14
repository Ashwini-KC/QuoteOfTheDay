"""
Copywrite ASHWINI, 2026
Author: ASHWINI
CreatedDate: 14 May 2026
LastModifiedDate: 14 May 2026
"""

from flask import Blueprint, jsonify, request, current_app
from app.services.quote_service import QuoteService
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

api_bp = Blueprint("api", __name__)


@api_bp.route("/quote", methods=["GET"])
def get_quote():
    """Get quote of the day endpoint"""
    try:
        quote = QuoteService.get_quote_of_the_day(current_app.config["QUOTES_FILE"])
        logger.info("Quote API endpoint accessed successfully")
        return jsonify(quote.to_dict()), 200
    except FileNotFoundError as e:
        logger.error(f"Quotes file not found: {e}")
        return jsonify({"error": "Quotes data unavailable"}), 500
    except ValueError as e:
        logger.error(f"Value error: {e}")
        return jsonify({"error": "Invalid quotes data"}), 500
    except Exception as e:
        logger.error(f"Unexpected error in quote endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500


@api_bp.route("/quote/<int:index>", methods=["GET"])
def get_quote_by_index(index):
    """Get quote by index endpoint"""
    try:
        quote = QuoteService.get_quote_by_index(current_app.config["QUOTES_FILE"], index)
        
        if quote is None:
            logger.warning(f"Quote index out of range: {index}")
            return jsonify({"error": "Quote not found"}), 404
        
        logger.info(f"Retrieved quote at index {index}")
        return jsonify(quote.to_dict()), 200
    except Exception as e:
        logger.error(f"Error retrieving quote by index {index}: {e}")
        return jsonify({"error": "Internal server error"}), 500


@api_bp.route("/quote/random", methods=["GET"])
def get_random_quote():
    """Get random quote endpoint"""
    try:
        quote = QuoteService.get_random_quote(current_app.config["QUOTES_FILE"])
        logger.info("Random quote endpoint accessed")
        return jsonify(quote.to_dict()), 200
    except ValueError as e:
        logger.error(f"No quotes available: {e}")
        return jsonify({"error": "No quotes available"}), 500
    except Exception as e:
        logger.error(f"Error getting random quote: {e}")
        return jsonify({"error": "Internal server error"}), 500


@api_bp.route("/quote", methods=["POST", "PUT", "DELETE"])
def invalid_quote_method():
    """Disallow other HTTP methods on quote endpoint"""
    logger.warning(f"Invalid method {request.method} on /api/quote endpoint")
    return jsonify({"error": "Method not allowed"}), 405


@api_bp.route("/quote/random", methods=["POST", "PUT", "DELETE"])
def invalid_random_method():
    """Disallow other HTTP methods on random endpoint"""
    logger.warning(f"Invalid method {request.method} on /api/quote/random endpoint")
    return jsonify({"error": "Method not allowed"}), 405
