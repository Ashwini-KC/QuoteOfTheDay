"""
Copywrite EDUBEX, 2025
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
    text: str
    author: str
    date_index: int
    category: Optional[str] = None
    tags: Optional[list] = None
    
    def to_dict(self):
        """Convert quote to dictionary"""
        return {
            "text": self.text,
            "author": self.author,
            "date_index": self.date_index,
            "category": self.category,
            "tags": self.tags or [],
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Quote":
        """Create Quote instance from dictionary"""
        return cls(
            text=data.get("text", ""),
            author=data.get("author", "Unknown"),
            date_index=data.get("date_index", 0),
            category=data.get("category"),
            tags=data.get("tags"),
        )
    
    def __str__(self):
        return f'"{self.text}" - {self.author}'
