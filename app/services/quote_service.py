"""
Copywrite ASHWINI, 2026
Author: ASHWINI
CreatedDate: 14 May 2026
LastModifiedDate: 14 May 2026
"""

import json
import os
from datetime import datetime
from typing import Optional, List
from app.models.quote import Quote
from app.utils.logger import setup_logger
from app.utils.validators import validate_quotes_data

logger = setup_logger(__name__)


class QuoteService:
    """Service for managing quotes"""
    
    _quotes_cache: Optional[List[Quote]] = None
    _cache_path: Optional[str] = None
    
    @classmethod
    def load_quotes(cls, quotes_file: str) -> List[Quote]:
        """
        Load quotes from JSON file with caching
        
        Args:
            quotes_file: Path to quotes.json file
            
        Returns:
            List of Quote objects
            
        Raises:
            FileNotFoundError: If quotes file doesn't exist
            json.JSONDecodeError: If JSON is malformed
        """
        # Return cached quotes if file path hasn't changed
        if cls._quotes_cache is not None and cls._cache_path == quotes_file:
            logger.info("Returning cached quotes")
            return cls._quotes_cache
        
        logger.info(f"Loading quotes from {quotes_file}")
        
        if not os.path.exists(quotes_file):
            logger.error(f"Quotes file not found: {quotes_file}")
            raise FileNotFoundError(f"Quotes file not found: {quotes_file}")
        
        try:
            with open(quotes_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Malformed JSON in quotes file: {e}")
            raise
        except Exception as e:
            logger.error(f"Error reading quotes file: {e}")
            raise
        
        # Validate quotes data
        if not validate_quotes_data(data):
            logger.error("Quotes data validation failed")
            raise ValueError("Invalid quotes data structure")
        
        # Convert to Quote objects
        quotes = []
        for idx, quote_data in enumerate(data):
            try:
                quote = Quote.from_dict(quote_data)
                quote.date_index = idx
                quotes.append(quote)
            except Exception as e:
                logger.warning(f"Skipping invalid quote at index {idx}: {e}")
                continue
        
        logger.info(f"Loaded {len(quotes)} quotes successfully")
        
        # Cache the quotes
        cls._quotes_cache = quotes
        cls._cache_path = quotes_file
        
        return quotes
    
    @classmethod
    def get_quote_of_the_day(cls, quotes_file: str) -> Quote:
        """
        Get quote of the day based on current date
        
        Args:
            quotes_file: Path to quotes.json file
            
        Returns:
            Quote object for today
        """
        quotes = cls.load_quotes(quotes_file)
        
        if not quotes:
            logger.error("No quotes available")
            raise ValueError("No quotes available")
        
        # Calculate day of year (0-365)
        today = datetime.now()
        day_of_year = today.timetuple().tm_yday - 1  # 0-indexed
        
        # Handle leap years: if day 366 exists, use day 365 for non-leap years
        max_quotes = len(quotes)
        if day_of_year >= max_quotes:
            day_of_year = day_of_year % max_quotes
        
        quote = quotes[day_of_year]
        logger.info(f"Retrieved quote of the day for {today.date()}: {quote}")
        
        return quote
    
    @classmethod
    def get_quote_by_index(cls, quotes_file: str, index: int) -> Optional[Quote]:
        """
        Get quote by specific index
        
        Args:
            quotes_file: Path to quotes.json file
            index: Index of quote to retrieve
            
        Returns:
            Quote object or None if index out of range
        """
        quotes = cls.load_quotes(quotes_file)
        
        if 0 <= index < len(quotes):
            return quotes[index]
        
        logger.warning(f"Quote index out of range: {index}")
        return None
    
    @classmethod
    def get_random_quote(cls, quotes_file: str) -> Quote:
        """
        Get a random quote
        
        Args:
            quotes_file: Path to quotes.json file
            
        Returns:
            Random Quote object
        """
        import random
        quotes = cls.load_quotes(quotes_file)
        
        if not quotes:
            raise ValueError("No quotes available")
        
        quote = random.choice(quotes)
        return quote
    
    @classmethod
    def clear_cache(cls):
        """Clear the quotes cache"""
        cls._quotes_cache = None
        cls._cache_path = None
        logger.info("Quotes cache cleared")
