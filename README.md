# Home Search Kenya — launch starter

This project contains:
- `app.py`: Streamlit tenant search and landlord/caretaker registration UI.
- `payment_api.py`: separate FastAPI service for Daraja STK Push, payment records, callbacks, and payment-status checks.
- `.streamlit/secrets.toml.example`: Streamlit-side settings example.

## Important status
This is a starter scaffold, **not a ready-to-charge production system**. It uses clearly labelled sample listings. Real M-Pesa payments will not work until Safaricom approves the relevant business payment shortcode and Daraja production access, the environment variables are configured, and the callback URL is publicly reachable over HTTPS. Do not collect fees until those steps and end-to-end tests are complete.

## 1. Install
Use Python 3.11 or newer. In a terminal, from this folder:

```bash
python -m venv .venv
```

Windows:
```powershell
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Then:
```bash
pip install -r requirements.txt
```

## 2. Configure the payment API
Set these as environment variables in the server hosting `payment_api.py`. Do not put live secrets in source code or commit them to Git.

Required:
- `DARAJA_ENV=sandbox` (start with sandbox; use `production` only after approval)
- `DARAJA_CONSUMER_KEY`
- `DARAJA_CONSUMER_SECRET`
- `DARAJA_SHORTCODE`
- `DARAJA_PASSKEY`
- `DARAJA_CALLBACK_URL` (public HTTPS URL ending in `/payments/callback`)
- `REGISTRATION_FEE_KES=1300` (example only; set the actual KSh fee you publish)
- `PAYMENT_ADMIN_KEY` (long random secret for the admin payment report)

For Paybill STK Push, the transaction type is commonly `CustomerPayBillOnline`. For a Till, Safaricom may require `CustomerBuyGoodsOnline` and the correct shortcode configuration. Confirm the required values for your specific shortcode in the Daraja documentation/approval.

## 3. Run locally
Terminal 1:
```bash
uvicorn payment_api:app --host 127.0.0.1 --port 8000
```

Terminal 2:
```bash
streamlit run app.py
```

The default API address is `http://localhost:8000`. To change it, configure `PAYMENT_API_BASE` in Streamlit secrets or the environment. The app will deliberately refuse to unlock registration unless the API reports `paid`.

## 4. Callback requirement
Safaricom must be able to reach `DARAJA_CALLBACK_URL` from the public internet. `localhost` is not a valid production callback. Deploy the API on a host with HTTPS and configure the callback URL to that deployed API endpoint. Streamlit hosting and the payment API may be separate services.

## 5. Test safely
- Use Daraja sandbox credentials and sandbox test numbers first.
- Test success, cancellation, timeout, wrong phone, duplicate callbacks, delayed callbacks, and service downtime.
- Confirm a successful callback is followed by an STK Query; this scaffold keeps a payment pending if query confirmation is unavailable.
- Review the Daraja API's current requirements and your account's transaction type before production.
- Never ask users to tell you their M-Pesa PIN or OTP.

## 6. Before launch
This starter does not yet permanently save landlord profiles or property listings; after payment it displays a submission preview. Build that next using a persistent database, authentication, role-based access, secure file storage, admin verification/review, audit logs, backups, and published privacy/fee/refund terms. Do not collect ID scans in this prototype. Add rate limiting and stronger callback security/monitoring before taking real payments. Get the current USD/KES conversion and fee terms right before advertising a "$10" fee; the KSh amount here is only an example.
