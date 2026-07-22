import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import resend

app = Flask(__name__)
CORS(app, origins=[
    "https://schrader.co",
    "https://www.schrader.co",
    "https://schraderweb-azure.vercel.app"
])

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_TABLE = os.getenv("SUPABASE_TABLE", "form_submissions")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
NOTIFICATION_EMAIL = os.getenv("NOTIFICATION_EMAIL", "")
VTEXT_EMAIL = os.getenv("VTEXT_EMAIL", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", "noreply@prakhargupta.me")

required = {
    "SUPABASE_URL": SUPABASE_URL,
    "SUPABASE_KEY": SUPABASE_KEY,
}

missing = [k for k, v in required.items() if not v]
if missing:
    raise RuntimeError("Missing environment variables: " + ", ".join(missing))

if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY


def send_email_notification(submission: dict):
    if not RESEND_API_KEY:
        return None

    html_result = None
    if NOTIFICATION_EMAIL:
        to_list = [e.strip() for e in NOTIFICATION_EMAIL.split(",") if e.strip()]
        if to_list:
            service_formatted = str(submission.get('service', 'N/A')).replace('-', ' ').title()
            consent_text = 'Consented' if submission.get('consent') else 'Declined'
            consent_bg = '#e6f7ed' if submission.get('consent') else '#feebee'
            consent_color = '#1e7e34' if submission.get('consent') else '#c82333'

            try:
                template_path = os.path.join(os.path.dirname(__file__), 'email-form.html')
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_content = f.read()

                budget_section = ""
                if submission.get("budget_range"):
                    budget_section = f"""
                    <h3 style="color: #0b1c3f; margin-top: 24px; margin-bottom: 12px; font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.02em;">Project Budget</h3>
                    <div style="background-color: #f8fafc; border-left: 4px solid #ff9500; padding: 12px 16px; font-size: 14px; font-weight: 600; color: #1e293b; border-radius: 0 4px 4px 0;">
                      {submission['budget_range']}
                    </div>
                    """

                message_section = ""
                if submission.get("message"):
                    message_section = f"""
                    <h3 style="color: #0b1c3f; margin-top: 28px; margin-bottom: 12px; font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.02em;">Project Details / Message</h3>
                    <div style="background-color: #f8fafc; border-left: 4px solid #0b1c3f; padding: 16px; font-size: 14px; color: #334155; border-radius: 0 4px 4px 0; white-space: pre-wrap; font-style: italic; line-height: 1.5;">
                      "{submission['message']}"
                    </div>
                    """

                html = template_content.format(
                    name=f"{submission['first_name']} {submission['last_name']}",
                    phone=submission['phone'],
                    email=submission.get('email', 'N/A'),
                    email_raw=submission.get('email', ''),
                    company=submission.get('company') or 'N/A',
                    service=service_formatted,
                    consent_bg=consent_bg,
                    consent_color=consent_color,
                    consent_text=consent_text,
                    budget_section=budget_section,
                    message_section=message_section
                )

                html_result = resend.Emails.send({
                    "from": EMAIL_FROM,
                    "to": to_list,
                    "subject": f"New Lead: {submission['first_name']} {submission['last_name']} - {service_formatted}",
                    "html": html,
                })
            except Exception as e:
                import sys
                print(f"Error sending HTML notification: {e}", file=sys.stderr)

    vtext_result = None
    if VTEXT_EMAIL:
        vtext_list = [e.strip() for e in VTEXT_EMAIL.split(",") if e.strip()]
        if vtext_list:
            # Structured, clean plain text message tailored for vtext/SMS viewability and character limits
            plain_text = f"""New Lead:
Name: {submission['first_name']} {submission['last_name']}
Phone: {submission['phone']}
Email: {submission.get('email', 'N/A')}
Company: {submission.get('company', 'N/A')}
Service: {submission.get('service', 'N/A')}"""

            if submission.get("budget_range"):
                plain_text += f"\nBudget: {submission['budget_range']}"
            if submission.get("message"):
                plain_text += f"\nMsg: {submission['message']}"

            try:
                vtext_result = resend.Emails.send({
                    "from": EMAIL_FROM,
                    "to": vtext_list,
                    "subject": "New Lead",
                    "text": plain_text,
                })
            except Exception as e:
                import sys
                print(f"Error sending SMS vtext notification: {e}", file=sys.stderr)

    return html_result or vtext_result


@app.route("/", methods=["GET"])
@app.route("/api", methods=["GET"])
@app.route("/api/", methods=["GET"])
def home():
    return jsonify({"ok": True, "message": "Form API is running"})


@app.route("/", methods=["POST"])
@app.route("/api", methods=["POST"])
@app.route("/api/", methods=["POST"])
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

        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }

        payloads = [row, {**row_base, "company": company or None}, row_base]

        inserted_data = None
        for payload in payloads:
            resp = requests.post(
                f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}",
                json=payload,
                headers=headers,
                timeout=10,
            )
            if resp.ok:
                inserted_data = resp.json()
                break

        email_result = send_email_notification(row)

        return jsonify({
            "success": True,
            "message": "Form submitted successfully",
            "data": inserted_data,
            "email_notified": email_result is not None,
        }), 200

    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    print(f"Starting dev server on port {port}...")
    app.run(host="127.0.0.1", port=port, debug=True)

