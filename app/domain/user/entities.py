from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    name: str
    email: str
    password_hash: str
    created_at: datetime
    updated_at: datetime
    user_id: Optional[int] = None
