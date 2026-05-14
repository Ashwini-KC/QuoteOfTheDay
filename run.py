"""
Copywrite EDUBEX, 2025
Author: ASHWINI
CreatedDate: 14 May 2026
LastModifiedDate: 14 May 2026
"""

from app import create_app, db
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

app = create_app()

if __name__ == "__main__":
    logger.info("Starting QuoteOfTheDay Flask application")
    app.run(debug=app.config["DEBUG"])
