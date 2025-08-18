import frappe
from frappe.utils import now, nowdate
from urllib.parse import urlparse
import re


def normalize_linkedin_url(url: str) -> str:
    if not url:
        return ""
    url = url.strip()
    # ensure scheme
    if url.startswith("//"):
        url = "https:" + url
    if not url.startswith("http"):
        url = "https://" + url
    # lowercase domain & path
    p = urlparse(url)
    host = p.netloc.lower()
    path = re.sub(r"/+$", "", p.path.lower())  # remove trailing slash
    # keep only /in/<slug> pattern
    m = re.match(r"^/in/[^/]+$", path)
    if not m:
        # sometimes links come as /in/<slug>/details/...
        m2 = re.match(r"^/in/([^/]+)/.*$", path)
        if m2:
            path = f"/in/{m2.group(1)}"
        else:
            return ""
    return f"https://www.linkedin.com{path}"


@frappe.whitelist(allow_guest=False, methods=["POST"])
def receive_pending():
    """
    Payload (JSON):
    {
      "account": "Account1",                  # must match Lead.linkedin_invited_by
      "pending_urls": ["https://.../in/slug", ...],
      "run_id": "optional-uuid",
      "scraped_at": "2025-08-18T12:00:00Z"
    }
    """
    payload = frappe.request.get_json() if hasattr(frappe.request, "get_json") else None
    if not payload:
        payload = frappe.parse_json(frappe.request.data)

    account = (payload.get("account") or "").strip()
    pending_urls_raw = payload.get("pending_urls") or []

    # Normalize incoming URLs
    pending_norm = set()
    for u in pending_urls_raw:
        nu = normalize_linkedin_url(u)
        if nu:
            pending_norm.add(nu)

    if not account:
        frappe.throw("Missing 'account' in payload.")
    # Fetch relevant leads
    lead_filters = {
        "linkedin_status": [
            "in",
            ["Connection Request Sent", "Connection Request Not Accepted"],
        ],
        "linkedin_invited_by": account,
    }
    leads = frappe.get_all(
        "CRM Lead",
        filters=lead_filters,
        fields=["name", "linkedin_url", "linkedin_status"],
    )

    to_connect = []
    still_pending = 0

    for ld in leads:
        ld_url_norm = normalize_linkedin_url(ld.get("linkedin_url"))
        if not ld_url_norm:
            # Skip leads without a valid linkedin_url
            continue

        if ld_url_norm in pending_norm:
            # Still pending
            still_pending += 1
            frappe.db.set_value("CRM Lead", ld["name"], "last_linkedin_check", now())
        else:
            # Not in pending list anymore → likely accepted
            to_connect.append(ld["name"])

    # Bulk update connected
    for name in to_connect:
        frappe.db.set_value(
            "CRM Lead",
            name,
            {
                "linkedin_status": "Connected",
                "linkedin_connected_on": nowdate(),
                "last_linkedin_check": now(),
            },
        )

    frappe.db.commit()

    return {
        "account": account,
        "received_pending_count": len(pending_norm),
        "updated_connected_count": len(to_connect),
        "still_pending_count": still_pending,
    }
