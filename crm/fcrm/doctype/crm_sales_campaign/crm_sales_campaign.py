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
                "width": "12rem",
            },
            {
                "label": "Target Market",
                "type": "Link",
                "key": "target_market",
                "options": "CRM Industry",
                "width": "12rem",
            },
            {
                "label": "Status",
                "type": "Select",
                "key": "campaign_status",
                "width": "8rem",
            },
            {
                "label": "Campaign Owner",
                "type": "Link",
                "key": "campaign_owner",
                "width": "10rem",
            },
            {
				"label": "Last Modified",
				"type": "Datetime",
				"key": "modified",
				"width": "12rem",
			},
        ]
        rows = [
            "sales_campaign",
            "target_territory",
            "target_market",
            "campaign_status",
            "campaign_owner",
            "modified",
        ]
        return {"columns": columns, "rows": rows}
