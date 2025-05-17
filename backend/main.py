from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from supabase_client import supabase

# ----------------------------
# FastAPI App Setup
# ----------------------------

app = FastAPI()

# Allow all CORS (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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

# ----------------------------
# Routes
# ----------------------------

@app.get("/")
def welcome():
    return {"message": "Welcome to the Unified UPI System (UUPI) 🚀"}


@app.get("/balance/{upi_id}")
def get_balance(upi_id: str):
    response = supabase.table("users").select("balance").eq("upi_id", upi_id).execute()
    user = response.data[0]

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"upi_id": upi_id, "balance": user["balance"]}


@app.post("/send")
def send_money(request: SendMoneyRequest):
    try:
        print("Handling send request...")

        sender_response = supabase.table("users").select("*").eq("upi_id", request.payer_id).execute()
        sender = sender_response.data
        if not sender:
            raise HTTPException(status_code=404, detail="Sender not found")
        

    # Step 2: Fetch receiver
        receiver_response = supabase.table("users").select("*").eq("upi_id", request.payee_id).execute()
        receiver = receiver_response.data
        if not receiver:
            raise HTTPException(status_code=404, detail="Receiver not found")

        # Step 3: Check balance
        if sender["balance"] < request.amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")

        # Step 4: Update balances
        new_sender_balance = sender["balance"] - request.amount
        new_receiver_balance = receiver["balance"] + request.amount

        # Step 5: Update sender
        sender_update = supabase.table("users").update({"balance": new_sender_balance}).eq("upi_id", request.payer_id).execute()
        if sender_update.error:
            raise HTTPException(status_code=500, detail="Failed to update sender balance")

        # Step 6: Update receiver
        receiver_update = supabase.table("users").update({"balance": new_receiver_balance}).eq("upi_id", request.payee_id).execute()
        if receiver_update.error:
            raise HTTPException(status_code=500, detail="Failed to update receiver balance")

        # Step 7: Log transaction
        txn = {
            "payer_id": request.payer_id,
            "payee_id": request.payee_id,
            "amount": request.amount,
            "timestamp": datetime.utcnow().isoformat()
        }

        txn_insert = supabase.table("transactions").insert(txn).single().execute()
        if txn_insert.error:
            raise HTTPException(status_code=500, detail="Transaction logging failed")

        return {"message": "✅ Transfer successful", "transaction": txn}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/transactions/{upi_id}")
def get_transactions(upi_id: str):
    response = supabase.table("transactions").select("*").or_(
        f"payer_id.eq.{upi_id},payee_id.eq.{upi_id}"
    ).order("timestamp", desc=True).execute()

    if response.error:
        raise HTTPException(status_code=500, detail="Failed to fetch transactions")

    return {"upi_id": upi_id, "transactions": response.data}
