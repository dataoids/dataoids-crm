# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CRMLinkedInChatSequence(Document):


    @staticmethod
    def default_list_data():
        columns = [
            {
                "label": "Sequence Number",
                "type": "Int",
                "key": "sequence_number",
                "width": "4rem",
            },
            {
                "label": "Sequence Delay",
                "type": "Duration",
                "key": "sequence_delay",
                "width": "8rem",
            },
            {
                "label": "Sequence Message",
                "type": "Text Editor",
                "key": "sequence_message",
                "width": "20rem",
            },
        ]
        rows = [
			"name",
			"sequence_number",
			"sequence_delay",
			"sequence_message",
            "modified",
        ]
        return {"columns": columns, "rows": rows}

