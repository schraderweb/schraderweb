import os
from flask import Flask, request, jsonify
from supabase import create_client
from twilio.rest import Client as TwilioClient

app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
BUSINESS_OWNER_PHONE = os.getenv("BUSINESS_OWNER_PHONE")
SUPABASE_TABLE = os.getenv("SUPABASE_TABLE", "form_submissions")

required = {
    "SUPABASE_URL": SUPABASE_URL,
    "SUPABASE_KEY": SUPABASE_KEY,
    "TWILIO_ACCOUNT_SID": TWILIO_ACCOUNT_SID,
    "TWILIO_AUTH_TOKEN": TWILIO_AUTH_TOKEN,
    "TWILIO_PHONE_NUMBER": TWILIO_PHONE_NUMBER,
    "BUSINESS_OWNER_PHONE": BUSINESS_OWNER_PHONE,
}

missing = [k for k, v in required.items() if not v]
if missing:
    raise RuntimeError("Missing environment variables: " + ", ".join(missing))

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
twilio_client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def normalize_phone(value: str) -> str:
    return str(value or "").strip()


def send_sms(to_number: str, body: str) -> str:
    message = twilio_client.messages.create(
        body=body,
        from_=TWILIO_PHONE_NUMBER,
        to=to_number,
    )
    return message.sid


@app.get("/")
def home():
    return jsonify({"ok": True, "message": "Form API is running"})


@app.post("/")
def submit_form():
    try:
        data = request.get_json(silent=True) or request.form.to_dict() or {}

        name = str(data.get("name", "")).strip()
        phone = normalize_phone(data.get("phone"))
        email = str(data.get("email", "")).strip()
        message_text = str(data.get("message", "")).strip()

        if not name or not phone:
            return jsonify({
                "success": False,
                "error": "name and phone are required"
            }), 400

        inserted = (
            supabase
            .table(SUPABASE_TABLE)
            .insert({
                "name": name,
                "phone": phone,
                "email": email,
                "message": message_text,
            })
            .execute()
        )

        customer_sid = send_sms(
            phone,
            f"Hi {name}, we received your form and will get back to you soon."
        )

        owner_sid = send_sms(
            BUSINESS_OWNER_PHONE,
            "New form submission received\n"
            f"Name: {name}\n"
            f"Phone: {phone}\n"
            f"Email: {email or 'N/A'}\n"
            f"Message: {message_text or 'N/A'}"
        )

        return jsonify({
            "success": True,
            "message": "Form submitted successfully",
            "data": inserted.data,
            "customer_sms_sid": customer_sid,
            "owner_sms_sid": owner_sid,
        }), 200

    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500
