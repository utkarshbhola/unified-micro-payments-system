from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI()

# ----------------------------
# Dummy DBs (Dicts for now)
# ----------------------------

users = {
    "utkarsh@umps": {"name": "Utkarsh", "balance": 5000},
    "rahul@umps": {"name": "Rahul", "balance": 3000},
}

transactions = []  # list of transaction records


# ----------------------------
# Pydantic Models
# ----------------------------

class SendMoneyRequest(BaseModel):
    sender_upi: str
    receiver_upi: str
    amount: float


class Transaction(BaseModel):
    sender_upi: str
    receiver_upi: str
    amount: float
    timestamp: str


# ----------------------------
# Routes
# ----------------------------

@app.get("/")
def welcome():
    return {"message": "Welcome to the Unified UPI System (UUPI) 🚀"}


@app.get("/balance/{upi_id}")
def get_balance(upi_id: str):
    user = users.get(upi_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"upi_id": upi_id, "balance": user["balance"]}


@app.post("/send")
def send_money(request: SendMoneyRequest):
    sender = users.get(request.sender_upi)
    receiver = users.get(request.receiver_upi)

    if not sender or not receiver:
        raise HTTPException(status_code=404, detail="Invalid sender or receiver")

    if sender["balance"] < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # Transfer logic
    sender["balance"] -= request.amount
    receiver["balance"] += request.amount

    txn = Transaction(
        sender_upi=request.sender_upi,
        receiver_upi=request.receiver_upi,
        amount=request.amount,
        timestamp=datetime.now().isoformat()
    )
    transactions.append(txn.dict())

    return {"message": "Transfer successful", "transaction": txn}


@app.get("/transactions/{upi_id}")
def get_transactions(upi_id: str):
    user_txns = [
        txn for txn in transactions
        if txn["sender_upi"] == upi_id or txn["receiver_upi"] == upi_id
    ]
    return {"upi_id": upi_id, "transactions": user_txns}
