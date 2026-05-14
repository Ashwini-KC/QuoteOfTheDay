"""
Copywrite EDUBEX, 2025
Author: ASHWINI
CreatedDate: 14 May 2026
LastModifiedDate: 14 May 2026
"""

from typing import Any, List


def validate_quotes_data(data: Any) -> bool:
    """
    Validate that quotes data has the correct structure
    
    Args:
        data: Data to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Must be a list
    if not isinstance(data, list):
        return False
    
    # Must not be empty
    if len(data) == 0:
        return False
    
    # Each item must be a dictionary with required fields
    for item in data:
        if not isinstance(item, dict):
            return False
        
        # Required fields
        if "text" not in item or "author" not in item:
            return False
        
        # Fields must be strings (or null for optional fields)
        if not isinstance(item["text"], str) or not isinstance(item["author"], str):
            return False
        
        # Text and author must not be empty
        if not item["text"].strip() or not item["author"].strip():
            return False
    
    return True


def validate_quote_text(text: str) -> bool:
    """
    Validate a quote text
    
    Args:
        text: Text to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(text, str):
        return False
    
    if len(text.strip()) == 0:
        return False
    
    if len(text) > 5000:
        return False
    
    return True


def validate_quote_author(author: str) -> bool:
    """
    Validate a quote author
    
    Args:
        author: Author to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(author, str):
        return False
    
    if len(author.strip()) == 0:
        return False
    
    if len(author) > 500:
        return False
    
    return True


def sanitize_string(value: str) -> str:
    """
    Sanitize a string by stripping whitespace
    
    Args:
        value: String to sanitize
        
    Returns:
        Sanitized string
    """
    if not isinstance(value, str):
        return ""
    
    return value.strip()
