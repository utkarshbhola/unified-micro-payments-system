from pydantic import BaseModel
from typing import Optional

class SendRequest(BaseModel):
    payer_id: str
    payee_id: str
    amount: float
    method: Optional[str] = "wallet"  # or upi

class BalanceRequest(BaseModel):
    user_id: str

class Transaction(BaseModel):
    payer_id: str
    payee_id: str
    amount: float
    method: str
    status: str
