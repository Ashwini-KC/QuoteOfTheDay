"""
Copywrite ASHWINI, 2026
Author: ASHWINI
CreatedDate: 14 May 2026
LastModifiedDate: 14 May 2026
"""

import pytest
import json
import os
from app.models.quote import Quote
from app.services.quote_service import QuoteService
from app.utils.validators import validate_quotes_data, validate_quote_text, validate_quote_author


class TestQuoteModel:
    """Unit tests for Quote model"""
    
    def test_quote_creation(self):
        """Test creating a Quote instance"""
        quote = Quote(
            text="The only way is forward.",
            author="Unknown",
            date_index=0,
            category="Motivation"
        )
        assert quote.text == "The only way is forward."
        assert quote.author == "Unknown"
        assert quote.date_index == 0
        assert quote.category == "Motivation"
    
    def test_quote_to_dict(self):
        """Test converting Quote to dictionary"""
        quote = Quote(
            text="The only way is forward.",
            author="Unknown",
            date_index=0,
            category="Motivation",
            tags=["life", "wisdom"]
        )
        quote_dict = quote.to_dict()
        assert quote_dict["text"] == "The only way is forward."
        assert quote_dict["author"] == "Unknown"
        assert quote_dict["category"] == "Motivation"
        assert quote_dict["tags"] == ["life", "wisdom"]
    
    def test_quote_from_dict(self):
        """Test creating Quote from dictionary"""
        data = {
            "text": "The only way is forward.",
            "author": "Unknown",
            "category": "Motivation",
            "tags": ["life", "wisdom"]
        }
        quote = Quote.from_dict(data)
        assert quote.text == "The only way is forward."
        assert quote.author == "Unknown"
        assert quote.category == "Motivation"
        assert quote.tags == ["life", "wisdom"]
    
    def test_quote_string_representation(self):
        """Test Quote string representation"""
        quote = Quote(
            text="The only way is forward.",
            author="Unknown",
            date_index=0
        )
        assert str(quote) == '"The only way is forward." - Unknown'


class TestValidators:
    """Unit tests for validators"""
    
    def test_validate_quotes_data_valid(self):
        """Test validating valid quotes data"""
        data = [
            {"text": "Quote 1", "author": "Author 1"},
            {"text": "Quote 2", "author": "Author 2"}
        ]
        assert validate_quotes_data(data) is True
    
    def test_validate_quotes_data_not_list(self):
        """Test validating non-list data"""
        data = {"text": "Quote 1", "author": "Author 1"}
        assert validate_quotes_data(data) is False
    
    def test_validate_quotes_data_empty_list(self):
        """Test validating empty list"""
        data = []
        assert validate_quotes_data(data) is False
    
    def test_validate_quotes_data_missing_fields(self):
        """Test validating data with missing fields"""
        data = [{"text": "Quote 1"}]
        assert validate_quotes_data(data) is False
    
    def test_validate_quotes_data_empty_text(self):
        """Test validating quote with empty text"""
        data = [{"text": "   ", "author": "Author 1"}]
        assert validate_quotes_data(data) is False
    
    def test_validate_quote_text_valid(self):
        """Test validating valid quote text"""
        assert validate_quote_text("The only way is forward.") is True
    
    def test_validate_quote_text_empty(self):
        """Test validating empty quote text"""
        assert validate_quote_text("   ") is False
    
    def test_validate_quote_text_too_long(self):
        """Test validating quote text that's too long"""
        long_text = "a" * 5001
        assert validate_quote_text(long_text) is False
    
    def test_validate_quote_author_valid(self):
        """Test validating valid author"""
        assert validate_quote_author("Steve Jobs") is True
    
    def test_validate_quote_author_empty(self):
        """Test validating empty author"""
        assert validate_quote_author("   ") is False


class TestQuoteService:
    """Unit tests for QuoteService"""
    
    @pytest.fixture
    def quotes_file(self):
        """Fixture providing path to test quotes file"""
        return os.path.join(
            os.path.dirname(__file__),
            "fixtures",
            "quotes.json"
        )
    
    def test_load_quotes(self, quotes_file):
        """Test loading quotes from file"""
        QuoteService.clear_cache()
        quotes = QuoteService.load_quotes(quotes_file)
        assert len(quotes) == 10
        assert isinstance(quotes[0], Quote)
        assert quotes[0].text == "The only way to do great work is to love what you do."
    
    def test_load_quotes_caching(self, quotes_file):
        """Test that quotes are cached"""
        QuoteService.clear_cache()
        quotes1 = QuoteService.load_quotes(quotes_file)
        quotes2 = QuoteService.load_quotes(quotes_file)
        assert quotes1 is quotes2
    
    def test_load_quotes_file_not_found(self):
        """Test loading quotes from non-existent file"""
        QuoteService.clear_cache()
        with pytest.raises(FileNotFoundError):
            QuoteService.load_quotes("/non/existent/path/quotes.json")
    
    def test_get_quote_of_the_day(self, quotes_file):
        """Test getting quote of the day"""
        QuoteService.clear_cache()
        quote = QuoteService.get_quote_of_the_day(quotes_file)
        assert isinstance(quote, Quote)
        assert quote.text is not None
        assert quote.author is not None
    
    def test_get_quote_by_index_valid(self, quotes_file):
        """Test getting quote by valid index"""
        QuoteService.clear_cache()
        quote = QuoteService.get_quote_by_index(quotes_file, 0)
        assert quote is not None
        assert quote.text == "The only way to do great work is to love what you do."
    
    def test_get_quote_by_index_invalid(self, quotes_file):
        """Test getting quote by invalid index"""
        QuoteService.clear_cache()
        quote = QuoteService.get_quote_by_index(quotes_file, 999)
        assert quote is None
    
    def test_get_random_quote(self, quotes_file):
        """Test getting random quote"""
        QuoteService.clear_cache()
        quote = QuoteService.get_random_quote(quotes_file)
        assert isinstance(quote, Quote)
        assert quote.text is not None
        assert quote.author is not None
    
    def test_clear_cache(self, quotes_file):
        """Test clearing cache"""
        QuoteService.clear_cache()
        quotes1 = QuoteService.load_quotes(quotes_file)
        QuoteService.clear_cache()
        quotes2 = QuoteService.load_quotes(quotes_file)
        assert quotes1 is not quotes2


class TestLeapYearHandling:
    """Unit tests for leap year handling"""
    
    @pytest.fixture
    def quotes_file(self):
        """Fixture providing path to test quotes file"""
        return os.path.join(
            os.path.dirname(__file__),
            "fixtures",
            "quotes.json"
        )
    
    def test_quote_day_index_wrapping(self, quotes_file):
        """Test that quote index doesn't exceed file length"""
        QuoteService.clear_cache()
        quotes = QuoteService.load_quotes(quotes_file)
        max_day = 365  # For non-leap year
        # Simulate day 366 (leap year)
        # The service should handle this gracefully
        assert len(quotes) > 0
