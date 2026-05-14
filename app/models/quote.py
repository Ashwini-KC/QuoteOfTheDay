"""
Copywrite ASHWINI, 2026
Author: ASHWINI
CreatedDate: 14 May 2026
LastModifiedDate: 14 May 2026
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Quote:
    """Quote model representing a single quote"""
    quote: str
    author: str
    date_index: int
    category: Optional[str] = None
    tags: Optional[list] = None
    
    def to_dict(self):
        """Convert quote to dictionary"""
        return {
            "quote": self.quote,
            "author": self.author,
            "date_index": self.date_index,
            "category": self.category,
            "tags": self.tags or [],
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Quote":
        """Create Quote instance from dictionary"""
        return cls(
            quote=data.get("quote", ""),
            author=data.get("author", "Unknown"),
            date_index=data.get("date_index", 0),
            category=data.get("category"),
            tags=data.get("tags"),
        )
    
    def __str__(self):
        return f'"{self.quote}" - {self.author}'
