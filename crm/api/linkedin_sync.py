import frappe
from frappe.utils import now, get_datetime, add_to_date
from crm.utils.linkedin import normalize_linkedin_url


@frappe.whitelist(allow_guest=False, methods=["POST"])
def receive_linkedin_lead_update():
    """
    Receives LinkedIn lead data from external automation tools (e.g. Waalaxy)
    and updates CRM Lead accordingly.

    Expected JSON body:
    {
      "_id": "68ac2f288cfef855aa033866",
      "firstName": "John",
      "lastName": "Doe",
      "linkedinUrl": "https://linkedin.com/in/johndoe",
      "connectedAt": "2025-04-16",
      "connectionRequestDate": "2025-04-16",
      "messageReplied": "Yes",
      "lastLinkedinMessageSentDate": "2025-04-16",
      "lastLinkedinReplyDate": "2025-04-16"
    }
    """

    payload = frappe.request.get_json(silent=True)
    if not payload:
        frappe.throw("Invalid or missing JSON payload.")

    linkedin_url = normalize_linkedin_url(payload.get("linkedinUrl") or "")
    if not linkedin_url:
        frappe.throw("Missing linkedinUrl in payload.")

    # Find leads with this LinkedIn URL
    leads = frappe.get_all(
        "CRM Lead",
        filters={"linkedin_url": linkedin_url},
        fields=["name", "linkedin_status", "status"]
    )
    if not leads:
        frappe.throw(f"No CRM Lead found with LinkedIn URL: {linkedin_url}")

    lead = leads[0]
    updates = {}
    
    updates["last_linkedin_check"] = now()

    # --- 1. Connection updates ---
    connected_at = payload.get("connectedAt")
    if connected_at:
        updates["linkedin_connected_on"] = connected_at

        if lead["linkedin_status"] in ["New", "Ready for Connection", "Request Sent"]:
            updates["linkedin_status"] = "Connected"
            updates['next_follow_up_on'] = add_to_date(days=2)

    # --- 2. Connection Request Date ---
    if payload.get("connectionRequestDate"):
        updates["linkedin_connection_request_on"] = payload.get("connectionRequestDate")

    # --- 3. Replies ---
    if payload.get("messageReplied") == "Yes" or payload.get("lastLinkedinReplyDate"):
        updates["linkedin_replied_on"] = payload.get("lastLinkedinReplyDate")
        updates["linkedin_status"] = "Nurturing"
        if lead["status"] not in ["Converted", "Disqualified", "Nurturing"]:
            updates["status"] = "Replied"
        

    # --- 4. Basic person fields (optional sync, keep CRM fresh) ---
    if payload.get("firstName") or payload.get("lastName"):
        updates["first_name"] = payload.get("firstName") or ""
        updates["last_name"] = payload.get("lastName") or ""
        updates["name"] = payload.get("_id")

    # --- 5. Next Follow-up on ---
    msg_date = get_datetime(payload.get("lastLinkedinMessageSentDate"))
    reply_date = get_datetime(payload.get("lastLinkedinReplyDate"))
    if msg_date and reply_date:
        if reply_date > msg_date:
            updates['next_follow_up_on'] = add_to_date(hours=2)
    if not reply_date and msg_date:
        updates['next_follow_up_on'] = add_to_date(msg_date, days=2)
    if payload.get("messageReplied") == "Yes":
        updates['next_follow_up_on'] = add_to_date(hours=2)
    if not reply_date:
        updates['next_follow_up_on'] = add_to_date(days=2)
    
    # --- Save updates ---
    if updates:
        frappe.db.set_value("CRM Lead", lead['name'], updates)
        frappe.db.commit()

    return {
        "lead": lead['name'],
        "updated_fields": list(updates.keys()),
        "success": True
    }
