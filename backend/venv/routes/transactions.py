from fastapi import APIRouter, HTTPException
from models import SendRequest, BalanceRequest
#from db import supabase   #or your db logic

router = APIRouter()

@router.post("/send")
def send_money(req: SendRequest):
    # Basic fallback logic for micro-payment routing
    method = req.method
    status = "success"

    if method == "upi":
        # Simulate UPI failure
        status = "failed"
        method = "wallet"  # fallback

    data = {
        "payer_id": req.payer_id,
        "payee_id": req.payee_id,
        "amount": req.amount,
        "status": status,
        "method": method
    }

    #result = supabase.table("transactions").insert(data).execute()

    return {"message": f"Payment {status}", "method_used": method}


#@router.post("/balance")
#def get_balance(req: BalanceRequest):
    # Placeholder logic — ideally pull from Supabase `wallets` table
    #wallet_data = supabase.table("wallets").select("balance").eq("user_id", req.user_id).single().execute()
    #return {"balance": wallet_data.data["balance"]}##


#@router.get("/transactions/{user_id}")
#def get_transactions(user_id: str):
#    res = supabase.table("transactions").select("*").or_(f"payer_id.eq.{user_id},payee_id.eq.{user_id}").execute()
#    return {"transactions": res.data}
