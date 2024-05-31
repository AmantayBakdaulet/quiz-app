from typing import Any, Dict
from uuid import UUID

from pydantic import BaseModel

class SubmitOutput(BaseModel):
    is_correct: bool
    message: str
