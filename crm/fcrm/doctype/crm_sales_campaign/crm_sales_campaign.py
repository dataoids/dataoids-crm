from frappe.model.document import Document


class CRMSalesCampaign(Document):

    @staticmethod
    def default_list_data():
        columns = [
            {
                "label": "Sales Campaign",
                "type": "Data",
                "key": "sales_campaign",
                "width": "16rem",
            },
            {
                "label": "Territory",
                "type": "Link",
                "key": "target_territory",
                "width": "14rem",
            },
            {
                "label": "Target Market",
                "type": "Link",
                "key": "target_market",
                "options": "CRM Industry",
                "width": "14rem",
            },
            {
                "label": "Campaign Owner",
                "type": "Link",
                "key": "campaign_owner",
                "width": "14rem",
            },
            {
                "label": "End Date",
                "type": "Date",
                "key": "end_date",
                "width": "8rem",
            },
        ]
        rows = [
            "sales_campaign",
            "territory",
            "market",
            "owner",
            "end_date",
        ]
        return {"columns": columns, "rows": rows}
