"""
Copywrite ASHWINI, 2026
Author: ASHWINI
CreatedDate: 14 May 2026
LastModifiedDate: 14 May 2026
"""

import pytest
import json
import os
from app import create_app, db
from config import TestingConfig


@pytest.fixture
def app():
    """Create and configure a new app instance for each test"""
    app = create_app()
    app.config.from_object(TestingConfig)
    
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    """A test client for the app"""
    return app.test_client()


class TestHomepage:
    """Integration tests for homepage routes"""
    
    def test_homepage_returns_200(self, client):
        """Test that homepage returns 200 status"""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_homepage_returns_html(self, client):
        """Test that homepage returns HTML"""
        response = client.get("/")
        assert response.content_type == "text/html; charset=utf-8"
    
    def test_homepage_contains_quote(self, client):
        """Test that homepage contains a quote"""
        response = client.get("/")
        assert b"quote" in response.data.lower() or b"inspiration" in response.data.lower()
    
    def test_health_endpoint_returns_200(self, client):
        """Test that health endpoint returns 200"""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_endpoint_returns_json(self, client):
        """Test that health endpoint returns JSON"""
        response = client.get("/health")
        assert response.content_type == "application/json"
    
    def test_health_endpoint_returns_healthy_status(self, client):
        """Test that health endpoint returns healthy status"""
        response = client.get("/health")
        data = json.loads(response.data)
        assert data["status"] == "healthy"


class TestAPIEndpoints:
    """Integration tests for API endpoints"""
    
    def test_api_quote_returns_200(self, client):
        """Test that /api/quote returns 200"""
        response = client.get("/api/quote")
        assert response.status_code == 200
    
    def test_api_quote_returns_json(self, client):
        """Test that /api/quote returns JSON"""
        response = client.get("/api/quote")
        assert response.content_type == "application/json"
    
    def test_api_quote_has_required_fields(self, client):
        """Test that /api/quote response has required fields"""
        response = client.get("/api/quote")
        data = json.loads(response.data)
        assert "text" in data
        assert "author" in data
        assert "date_index" in data
    
    def test_api_quote_by_index_returns_200(self, client):
        """Test that /api/quote/<index> returns 200 for valid index"""
        response = client.get("/api/quote/0")
        assert response.status_code == 200
    
    def test_api_quote_by_index_returns_json(self, client):
        """Test that /api/quote/<index> returns JSON"""
        response = client.get("/api/quote/0")
        assert response.content_type == "application/json"
    
    def test_api_quote_by_index_returns_404_for_invalid_index(self, client):
        """Test that /api/quote/<index> returns 404 for invalid index"""
        response = client.get("/api/quote/99999")
        assert response.status_code == 404
    
    def test_api_random_quote_returns_200(self, client):
        """Test that /api/quote/random returns 200"""
        response = client.get("/api/quote/random")
        assert response.status_code == 200
    
    def test_api_random_quote_returns_json(self, client):
        """Test that /api/quote/random returns JSON"""
        response = client.get("/api/quote/random")
        assert response.content_type == "application/json"


class TestErrorHandling:
    """Integration tests for error handling"""
    
    def test_404_not_found(self, client):
        """Test that non-existent route returns 404"""
        response = client.get("/non/existent/route")
        assert response.status_code == 404
    
    def test_404_error_page_html(self, client):
        """Test that 404 error page is HTML"""
        response = client.get("/non/existent/route")
        assert response.content_type == "text/html; charset=utf-8"
    
    def test_invalid_method_on_quote_endpoint(self, client):
        """Test that POST method on /api/quote returns 405"""
        response = client.post("/api/quote")
        assert response.status_code == 405
    
    def test_invalid_method_returns_json(self, client):
        """Test that invalid method returns JSON error"""
        response = client.post("/api/quote")
        assert response.content_type == "application/json"
        data = json.loads(response.data)
        assert "error" in data


class TestEndpointSecurity:
    """Integration tests for security and data handling"""
    
    def test_quote_text_no_xss(self, client):
        """Test that quote text doesn't contain unescaped HTML"""
        response = client.get("/api/quote")
        data = json.loads(response.data)
        # Quotes should be plain text
        assert "<script>" not in data["text"].lower()
    
    def test_api_returns_safe_data(self, client):
        """Test that API returns safe data"""
        response = client.get("/api/quote")
        data = json.loads(response.data)
        # Verify data is properly structured
        assert isinstance(data["text"], str)
        assert isinstance(data["author"], str)
        assert isinstance(data["date_index"], int)
    
    def test_quote_index_is_within_bounds(self, client):
        """Test that returned quote index is valid"""
        response = client.get("/api/quote")
        data = json.loads(response.data)
        # Index should be reasonable
        assert data["date_index"] >= 0
        assert data["date_index"] < 1000


class TestMultipleQuotes:
    """Integration tests for multiple quote access patterns"""
    
    def test_can_get_multiple_quotes_sequentially(self, client):
        """Test that we can get multiple different quotes"""
        quotes = []
        for i in range(5):
            response = client.get(f"/api/quote/{i}")
            if response.status_code == 200:
                data = json.loads(response.data)
                quotes.append(data)
        
        assert len(quotes) == 5
        # First quotes should be different
        assert quotes[0]["text"] != quotes[1]["text"]
    
    def test_random_quotes_are_different(self, client):
        """Test that random quotes are varied"""
        random_quotes = []
        for _ in range(10):
            response = client.get("/api/quote/random")
            if response.status_code == 200:
                data = json.loads(response.data)
                random_quotes.append(data["text"])
        
        # At least some quotes should be different (statistically likely)
        unique_quotes = set(random_quotes)
        assert len(unique_quotes) > 1
