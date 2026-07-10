import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
import resend

app = Flask(__name__)
CORS(app)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_TABLE = os.getenv("SUPABASE_TABLE", "form_submissions")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
NOTIFICATION_EMAIL = os.getenv("NOTIFICATION_EMAIL", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", "noreply@prakhargupta.me")

required = {
    "SUPABASE_URL": SUPABASE_URL,
    "SUPABASE_KEY": SUPABASE_KEY,
}

missing = [k for k, v in required.items() if not v]
if missing:
    raise RuntimeError("Missing environment variables: " + ", ".join(missing))

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY


def send_email_notification(submission: dict):
    if not RESEND_API_KEY or not NOTIFICATION_EMAIL:
        return None

    to_list = [e.strip() for e in NOTIFICATION_EMAIL.split(",") if e.strip()]

    html = f"""
    <h2>New Form Submission</h2>
    <table style="border-collapse:collapse;width:100%">
      <tr><td style="padding:8px;border:1px solid #ddd;font-weight:700">Name</td>
          <td style="padding:8px;border:1px solid #ddd">{submission['first_name']} {submission['last_name']}</td></tr>
      <tr><td style="padding:8px;border:1px solid #ddd;font-weight:700">Phone</td>
          <td style="padding:8px;border:1px solid #ddd">{submission['phone']}</td></tr>
      <tr><td style="padding:8px;border:1px solid #ddd;font-weight:700">Email</td>
          <td style="padding:8px;border:1px solid #ddd">{submission.get('email', 'N/A')}</td></tr>
      <tr><td style="padding:8px;border:1px solid #ddd;font-weight:700">Company</td>
          <td style="padding:8px;border:1px solid #ddd">{submission.get('company', 'N/A')}</td></tr>
      <tr><td style="padding:8px;border:1px solid #ddd;font-weight:700">Service</td>
          <td style="padding:8px;border:1px solid #ddd">{submission.get('service', 'N/A')}</td></tr>
      <tr><td style="padding:8px;border:1px solid #ddd;font-weight:700">Consent</td>
          <td style="padding:8px;border:1px solid #ddd">{'Yes' if submission.get('consent') else 'No'}</td></tr>
    </table>
    """

    try:
        response = resend.Emails.send({
            "from": EMAIL_FROM,
            "to": to_list,
            "subject": f"New Support Form Submission - {submission['first_name']} {submission['last_name']}",
            "html": html,
        })
        return response
    except Exception:
        return None


@app.get("/")
def home():
    return jsonify({"ok": True, "message": "Form API is running"})


@app.post("/")
def submit_form():
    try:
        data = request.get_json(silent=True) or request.form.to_dict() or {}

        # Support single "name" field or split first/last names
        first_name = str(data.get("first_name", "")).strip()
        last_name = str(data.get("last_name", "")).strip()
        full_name = str(data.get("name", "")).strip()

        if full_name and not (first_name or last_name):
            parts = full_name.split(None, 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else "-"

        phone = str(data.get("phone", "")).strip()
        email = str(data.get("email", "")).strip()
        company = str(data.get("company", data.get("company_name", ""))).strip()
        service = str(data.get("service", data.get("service_interest", ""))).strip()
        consent = data.get("consent") in (True, "true", "on", "yes")

        # Additional fields from contact form
        message = str(data.get("message", "")).strip()
        budget_range = str(data.get("budget", data.get("budget_range", ""))).strip()

        if not first_name or not last_name or not phone:
            return jsonify({
                "success": False,
                "error": "first_name, last_name, and phone are required"
            }), 400

        # Try inserting the complete row including new columns
        row = {
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "email": email or None,
            "company": company or None,
            "service": service or None,
            "consent": consent,
            "message": message or None,
            "budget_range": budget_range or None,
        }

        # Safe fallback in case some schema configurations lack company/message/budget_range columns
        row_base = {
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "email": email or None,
            "service": service or None,
            "consent": consent,
        }

        try:
            inserted = (supabase.table(SUPABASE_TABLE).insert(row).execute())
        except Exception:
            try:
                row_with_company = {**row_base, "company": company or None}
                inserted = (supabase.table(SUPABASE_TABLE).insert(row_with_company).execute())
            except Exception:
                inserted = (supabase.table(SUPABASE_TABLE).insert(row_base).execute())

        email_result = send_email_notification(row)

        return jsonify({
            "success": True,
            "message": "Form submitted successfully",
            "data": inserted.data,
            "email_notified": email_result is not None,
        }), 200

    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    print(f"Starting dev server on port {port}...")
    app.run(host="127.0.0.1", port=port, debug=True)

