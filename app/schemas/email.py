from typing import List
from pydantic import BaseModel, EmailStr


class VerifyEmail(BaseModel):
    recipients: List[EmailStr]
    subject: str
    body: str
