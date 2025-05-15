from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, validator
from typing import Optional,List
from datetime import datetime
from routes import transactions
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transactions.router)

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
    payer_id: str
    payee_id: str
    amount: float = Field(..., gt=0)

    @field_validator('payer_id', 'payee_id')
    def check_upi_format(cls, v):
        if '@' not in v:
            raise ValueError("Invalid UPI ID format")
        return v


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
    print("Received request:", request)
    sender = users.get(request.payer_id)
    receiver = users.get(request.payee_id)

    if not sender or not receiver:
        raise HTTPException(status_code=404, detail="Invalid sender or receiver")

    if sender["balance"] < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # Transfer logic
    sender["balance"] -= request.amount
    receiver["balance"] += request.amount

    txn = Transaction(
        sender_upi=request.payer_id,
        receiver_upi=request.payee_id,
        amount=request.amount,
        timestamp=datetime.now().isoformat()
    )
    transactions.append(txn.model_dump())

    return {"message": "Transfer successful", "transaction": txn}


@app.get("/transactions/{upi_id}")
def get_transactions(upi_id: str):
    user_txns = [
        txn for txn in transactions
        if txn["sender_upi"] == upi_id or txn["receiver_upi"] == upi_id
    ]
    return {"upi_id": upi_id, "transactions": user_txns}
