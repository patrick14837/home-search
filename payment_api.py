import os
import re
import uuid
import base64
import sqlite3
from datetime import datetime
from typing import Optional

import requests
from fastapi import FastAPI, HTTPException, Request, Header
from pydantic import BaseModel, Field, EmailStr

DB_PATH = os.getenv("HOME_SEARCH_DB", "home_search_payments.sqlite3")
DARAJA_ENV = os.getenv("DARAJA_ENV", "sandbox").lower()
DARAJA_BASE = "https://api.safaricom.co.ke" if DARAJA_ENV == "production" else "https://sandbox.safaricom.co.ke"

app = FastAPI(title="Home Search Kenya Payment API", version="0.1.0")

def db():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            payment_id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            role TEXT NOT NULL,
            amount INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            merchant_request_id TEXT,
            checkout_request_id TEXT UNIQUE,
            mpesa_receipt TEXT,
            result_code TEXT,
            result_description TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """)
init_db()

class STKRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    phone: str
    email: Optional[str] = None
    role: str
    amount: int = Field(ge=1, le=150000)

def now():
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"

def normalize_phone(value: str) -> str:
    digits = re.sub(r"\D", "", value or "")
    if digits.startswith("0") and len(digits) == 10:
        digits = "254" + digits[1:]
    elif digits.startswith("7") and len(digits) == 9:
        digits = "254" + digits
    elif digits.startswith("1") and len(digits) == 9:
        digits = "254" + digits
    if not re.fullmatch(r"254[17]\d{8}", digits):
        raise HTTPException(status_code=400, detail="Enter a valid Kenyan M-Pesa phone number, e.g. 0712345678.")
    return digits

def daraja_config():
    required = ["DARAJA_CONSUMER_KEY", "DARAJA_CONSUMER_SECRET", "DARAJA_SHORTCODE", "DARAJA_PASSKEY", "DARAJA_CALLBACK_URL"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise HTTPException(status_code=503, detail="M-Pesa is not configured yet. Missing server settings: " + ", ".join(missing))
    return {k: os.environ[k] for k in required}

def access_token(cfg):
    try:
        response = requests.get(
            f"{DARAJA_BASE}/oauth/v1/generate?grant_type=client_credentials",
            auth=(cfg["DARAJA_CONSUMER_KEY"], cfg["DARAJA_CONSUMER_SECRET"]),
            timeout=20,
        )
        response.raise_for_status()
        return response.json()["access_token"]
    except (requests.RequestException, KeyError, ValueError):
        raise HTTPException(status_code=502, detail="Could not obtain an M-Pesa API token.")

def stk_password(shortcode, passkey, timestamp):
    raw = f"{shortcode}{passkey}{timestamp}"
    return base64.b64encode(raw.encode()).decode()

def daraja_timestamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")

@app.get("/health")
def health():
    return {"ok": True, "service": "Home Search Kenya payment API"}

@app.post("/payments/stk-push")
def create_stk_push(payload: STKRequest):
    cfg = daraja_config()
    phone = normalize_phone(payload.phone)
    if payload.role not in ("Landlord", "Caretaker / agent"):
        raise HTTPException(status_code=400, detail="Invalid registration role.")
    # The fee is controlled by server configuration, not trusted from the browser.
    expected_amount = int(os.getenv("REGISTRATION_FEE_KES", "1300"))
    if payload.amount != expected_amount:
        raise HTTPException(status_code=400, detail=f"The registration fee is currently KSh {expected_amount}.")
    payment_id = "HSK-" + uuid.uuid4().hex[:12].upper()
    timestamp = daraja_timestamp()
    shortcode = cfg["DARAJA_SHORTCODE"]
    token = access_token(cfg)
    body = {
        "BusinessShortCode": shortcode,
        "Password": stk_password(shortcode, cfg["DARAJA_PASSKEY"], timestamp),
        "Timestamp": timestamp,
        "TransactionType": os.getenv("DARAJA_TRANSACTION_TYPE", "CustomerPayBillOnline"),
        "Amount": expected_amount,
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": cfg["DARAJA_CALLBACK_URL"],
        "AccountReference": payment_id[:12],
        "TransactionDesc": "Home Search Kenya registration",
    }
    try:
        response = requests.post(
            f"{DARAJA_BASE}/mpesa/stkpush/v1/processrequest",
            json=body,
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
        data = response.json()
    except (requests.RequestException, ValueError):
        raise HTTPException(status_code=502, detail="Could not contact M-Pesa STK Push.")
    if response.status_code >= 400 or data.get("ResponseCode") != "0":
        message = data.get("errorMessage") or data.get("ResponseDescription") or "M-Pesa rejected the payment request."
        raise HTTPException(status_code=502, detail=message)

    created = now()
    with db() as conn:
        conn.execute("""
        INSERT INTO payments(payment_id, full_name, phone, email, role, amount, status,
          merchant_request_id, checkout_request_id, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, 'pending', ?, ?, ?, ?)
        """, (payment_id, payload.full_name.strip(), phone, payload.email, payload.role,
              expected_amount, data.get("MerchantRequestID"), data.get("CheckoutRequestID"), created, created))
    return {"payment_id": payment_id, "status": "pending", "customer_message": data.get("CustomerMessage", "Check your phone for the M-Pesa prompt.")}

def stk_query(checkout_request_id: str, cfg):
    """Ask Daraja for the authoritative transaction status before unlocking registration."""
    token = access_token(cfg)
    timestamp = daraja_timestamp()
    shortcode = cfg["DARAJA_SHORTCODE"]
    body = {
        "BusinessShortCode": shortcode,
        "Password": stk_password(shortcode, cfg["DARAJA_PASSKEY"], timestamp),
        "Timestamp": timestamp,
        "CheckoutRequestID": checkout_request_id,
    }
    try:
        response = requests.post(
            f"{DARAJA_BASE}/mpesa/stkpushquery/v1/query",
            json=body,
            headers={"Authorization": f"Bearer {token}"},
            timeout=20,
        )
        return response.json()
    except (requests.RequestException, ValueError):
        return {}

@app.post("/payments/callback")
async def payment_callback(request: Request):
    # Daraja callbacks are not treated as trusted just because they reach this URL.
    # A successful callback is followed by an STK Query before marking the payment paid.
    try:
        payload = await request.json()
        callback = payload["Body"]["stkCallback"]
        checkout_id = callback["CheckoutRequestID"]
    except (ValueError, KeyError, TypeError):
        raise HTTPException(status_code=400, detail="Malformed callback payload.")

    with db() as conn:
        row = conn.execute("SELECT * FROM payments WHERE checkout_request_id=?", (checkout_id,)).fetchone()
    if not row:
        # Acknowledge unknown callback without creating a payment record.
        return {"ResultCode": 0, "ResultDesc": "Callback received"}

    result_code = str(callback.get("ResultCode", "unknown"))
    description = str(callback.get("ResultDesc", ""))[:500]
    status = "failed"
    receipt = None

    if result_code == "0":
        cfg = daraja_config()
        query_result = stk_query(checkout_id, cfg)
        query_code = str(query_result.get("ResultCode", ""))
        if query_code == "0":
            status = "paid"
            items = callback.get("CallbackMetadata", {}).get("Item", [])
            for item in items:
                if item.get("Name") == "MpesaReceiptNumber":
                    receipt = str(item.get("Value", ""))[:40]
                    break
        else:
            # Never unlock based solely on an unconfirmed callback.
            status = "pending"
            description = (description + " | STK Query not yet confirmed").strip(" |")

    with db() as conn:
        conn.execute("""
        UPDATE payments SET status=?, mpesa_receipt=COALESCE(?, mpesa_receipt),
          result_code=?, result_description=?, updated_at=? WHERE checkout_request_id=?
        """, (status, receipt, result_code, description, now(), checkout_id))
    return {"ResultCode": 0, "ResultDesc": "Callback received"}

@app.get("/payments/{payment_id}")
def get_payment(payment_id: str):
    with db() as conn:
        row = conn.execute("""
        SELECT payment_id, status, amount, role, created_at, updated_at, mpesa_receipt
        FROM payments WHERE payment_id=?
        """, (payment_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Payment reference not found.")
    return dict(row)

@app.get("/admin/payments")
def list_payments(x_admin_key: Optional[str] = Header(default=None)):
    admin_key = os.getenv("PAYMENT_ADMIN_KEY")
    if not admin_key or not x_admin_key or x_admin_key != admin_key:
        raise HTTPException(status_code=403, detail="Not authorized.")
    with db() as conn:
        rows = conn.execute("""
        SELECT payment_id, full_name, phone, role, amount, status, mpesa_receipt, created_at
        FROM payments ORDER BY created_at DESC LIMIT 500
        """).fetchall()
    return [dict(r) for r in rows]
