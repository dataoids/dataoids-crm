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
                "label": "Target Market",
                "type": "Link",
                "key": "target_market",
                "options": "CRM Industry",
                "width": "12rem",
            },
            {
                "label": "Target Industry",
                "type": "Link",
                "key": "target_industry",
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
            "name",
            "sales_campaign",
            "target_market",
            "target_industry",
            "campaign_status",
            "campaign_owner",
            "modified",
        ]
        return {"columns": columns, "rows": rows}
