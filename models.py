from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Reel:

    url: str

    views_text: str
    views: int

    posted_date: Optional[datetime] = None

    likes_text: Optional[str] = None
    likes: Optional[int] = None