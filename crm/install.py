# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt
import click
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

from crm.fcrm.doctype.crm_dashboard.crm_dashboard import create_default_manager_dashboard
from crm.fcrm.doctype.crm_products.crm_products import create_product_details_script


def before_install():
	pass


def after_install(force=False):
	add_default_lead_statuses()
	add_default_linkedin_statuses()
	add_default_email_statuses()
	add_default_deal_statuses()
	add_default_communication_statuses()
	add_default_fields_layout(force)
	add_property_setter()
	add_email_template_custom_fields()
	add_default_industries()
	add_default_lead_sources()
	add_default_lost_reasons()
	add_standard_dropdown_items()
	add_default_scripts()
	create_default_manager_dashboard(force)
	frappe.db.commit()


def add_default_lead_statuses():
	statuses = {
		"New": {
			"color": "gray",
			"position": 1,
		},
		"Enriching": {
			"color": "cyan",
			"position": 2,
		},
		"Outreach in Progress": {
			"color": "blue",
			"position": 3,
		},
		"Replied": {
			"color": "green",
			"position": 4,
		},
		"Not Replied": {
			"color": "amber",
			"position": 4,
		},
		"Nurturing": {
			"color": "purple",
			"position": 6,
		},
		"Disqualified": {
			"color": "red",
			"position": 7,
		},
		"Converted": {
			"color": "green",
			"position": 8,
		},
	}

	for status in statuses:
		if frappe.db.exists("CRM Lead Status", status):
			continue

		doc = frappe.new_doc("CRM Lead Status")
		doc.lead_status = status
		doc.color = statuses[status]["color"]
		doc.position = statuses[status]["position"]
		doc.insert()


def add_default_linkedin_statuses():
	statuses = {
		"New": {
			"color": "gray",
			"position": 1,
		},
		"Ready for Connection Request": {
			"color": "cyan",
			"position": 2,
		},
		"Connection Request Sent": {
			"color": "blue",
			"position": 3,
		},
		"Connected": {
			"color": "green",
			"position": 4,
		},
		"Connection Request Not Accepted": {
			"color": "amber",
			"position": 4,
		},
		"Nurturing": {
			"color": "purple",
			"position": 6,
		},
		"Disqualified": {
			"color": "red",
			"position": 7,
		},
		"Converted": {
			"color": "green",
			"position": 8,
		},
	}

	for status in statuses:
		if frappe.db.exists("CRM Lead LinkedIn Status", status):
			continue

		doc = frappe.new_doc("CRM Lead LinkedIn Status")
		doc.linkedin_status = status
		doc.color = statuses[status]["color"]
		doc.position = statuses[status]["position"]
		doc.insert()


def add_default_email_statuses():
	statuses = {
		"New": {
			"color": "gray",
			"position": 1,
		},
		"Ready for Email": {
			"color": "cyan",
			"position": 2,
		},
		"Email Sent": {
			"color": "blue",
			"position": 3,
		},
		"Replied": {
			"color": "green",
			"position": 4,
		},
		"Not Replied": {
			"color": "amber",
			"position": 4,
		},
		"Nurturing": {
			"color": "purple",
			"position": 6,
		},
		"Disqualified": {
			"color": "red",
			"position": 7,
		},
		"Converted": {
			"color": "green",
			"position": 8,
		},
	}

	for status in statuses:
		if frappe.db.exists("CRM Lead Email Status", status):
			continue

		doc = frappe.new_doc("CRM Lead Email Status")
		doc.email_status = status
		doc.color = statuses[status]["color"]
		doc.position = statuses[status]["position"]
		doc.insert()


def add_default_deal_statuses():
	statuses = {
		"Qualification": {
			"color": "gray",
			"type": "Open",
			"probability": 10,
			"position": 1,
		},
		"Demo/Making": {
			"color": "orange",
			"type": "Ongoing",
			"probability": 25,
			"position": 2,
		},
		"Proposal/Quotation": {
			"color": "blue",
			"type": "Ongoing",
			"probability": 50,
			"position": 3,
		},
		"Negotiation": {
			"color": "yellow",
			"type": "Ongoing",
			"probability": 70,
			"position": 4,
		},
		"Ready to Close": {
			"color": "purple",
			"type": "Ongoing",
			"probability": 90,
			"position": 5,
		},
		"Won": {
			"color": "green",
			"type": "Won",
			"probability": 100,
			"position": 6,
		},
		"Lost": {
			"color": "red",
			"type": "Lost",
			"probability": 0,
			"position": 7,
		},
	}

	for status in statuses:
		if frappe.db.exists("CRM Deal Status", status):
			continue

		doc = frappe.new_doc("CRM Deal Status")
		doc.deal_status = status
		doc.color = statuses[status]["color"]
		doc.type = statuses[status]["type"]
		doc.probability = statuses[status]["probability"]
		doc.position = statuses[status]["position"]
		doc.insert()


def add_default_communication_statuses():
	statuses = ["Open", "Replied"]

	for status in statuses:
		if frappe.db.exists("CRM Communication Status", status):
			continue

		doc = frappe.new_doc("CRM Communication Status")
		doc.status = status
		doc.insert()


def add_default_fields_layout(force=False):
	quick_entry_layouts = {
		"CRM Lead-Quick Entry": {
			"doctype": "CRM Lead",
			"layout": '[{"name":"first_tab","sections":[{"name":"person_section","columns":[{"name":"column_5jrk","fields":["first_name","sales_campaign"]},{"name":"column_5CPV","fields":["last_name","organization"]}],"editingLabel":false,"label":"Primary Information"},{"name":"organization_section","columns":[{"name":"column_GHfX","fields":["job_title","job_title_category"]},{"name":"column_hXjS","fields":["gender","lead_type"]}],"editingLabel":false,"label":"Employee Information"},{"name":"lead_section","columns":[{"name":"column_EO1H","fields":["email"]},{"name":"column_RWBe","fields":["linkedin_url"]},{"label":"","name":"column_qLXX","fields":["mobile_no"]}],"editingLabel":false,"label":"Personal Information"},{"label":"Tracking Information","name":"section_hOQa","opened":true,"columns":[{"name":"column_VQhQ","fields":["source","status","linkedin_status"]},{"label":"","name":"column_jPcX","fields":["lead_score","lead_owner","email_status"]}],"editingLabel":false}]}]',
		},
		"CRM Deal-Quick Entry": {
			"doctype": "CRM Deal",
			"layout": '[{"name": "organization_section", "hidden": true, "editable": false, "columns": [{"name": "column_GpMP", "fields": ["organization"]}, {"name": "column_FPTn", "fields": []}]}, {"name": "organization_details_section", "editable": false, "columns": [{"name": "column_S3tQ", "fields": ["organization_name", "territory"]}, {"name": "column_KqV1", "fields": ["website", "annual_revenue"]}, {"name": "column_1r67", "fields": ["no_of_employees", "industry"]}]}, {"name": "contact_section", "hidden": true, "editable": false, "columns": [{"name": "column_CeXr", "fields": ["contact"]}, {"name": "column_yHbk", "fields": []}]}, {"name": "contact_details_section", "editable": false, "columns": [{"name": "column_ZTWr", "fields": ["salutation", "email"]}, {"name": "column_tabr", "fields": ["first_name", "mobile_no"]}, {"name": "column_Qjdx", "fields": ["last_name", "gender"]}]}, {"name": "deal_section", "columns": [{"name": "column_mdps", "fields": ["status"]}, {"name": "column_H40H", "fields": ["deal_owner"]}]}]',
		},
		"Contact-Quick Entry": {
			"doctype": "Contact",
			"layout": '[{"name": "salutation_section", "columns": [{"name": "column_eXks", "fields": ["salutation"]}]}, {"name": "full_name_section", "hideBorder": true, "columns": [{"name": "column_cSxf", "fields": ["first_name"]}, {"name": "column_yBc7", "fields": ["last_name"]}]}, {"name": "email_section", "hideBorder": true, "columns": [{"name": "column_tH3L", "fields": ["email_id"]}]}, {"name": "mobile_gender_section", "hideBorder": true, "columns": [{"name": "column_lrfI", "fields": ["mobile_no"]}, {"name": "column_Tx3n", "fields": ["gender"]}]}, {"name": "organization_section", "hideBorder": true, "columns": [{"name": "column_S0J8", "fields": ["company_name"]}]}, {"name": "designation_section", "hideBorder": true, "columns": [{"name": "column_bsO8", "fields": ["designation"]}]}, {"name": "address_section", "hideBorder": true, "columns": [{"name": "column_W3VY", "fields": ["address"]}]}]',
		},
		"CRM Organization-Quick Entry": {
			"doctype": "CRM Organization",
			"layout": '[{"name":"first_tab","sections":[{"name":"organization_section","columns":[{"name":"column_zOuv","fields":["sales_campaign","organization_name","website"]}],"editingLabel":false,"label":"Basic Information","collapsible":true},{"name":"website_revenue_section","hideBorder":true,"columns":[{"name":"column_I5Dy","fields":["territory","no_of_employees"]},{"label":"","name":"column_Uppr","fields":["industry","annual_revenue"]}],"editingLabel":false,"label":"Other Information","collapsible":true},{"name":"address_section","hideBorder":true,"columns":[{"name":"column_O2dk","fields":["address"]}]}]}]',
		},
  		"CRM Sales Campaign-Quick Entry": {
			"doctype": "CRM Sales Campaign",
			"layout": '[{"name":"tab_RZ0A","sections":[{"name":"section_wQcc","columns":[{"name":"column_tIkB","fields":["sales_campaign"]}]},{"name":"section_ReFT","columns":[{"name":"column_RVIG","fields":["target_market","campaign_owner","start_date"]},{"name":"column_LmjO","fields":["target_industry","campaign_status","end_date"]}]}]}]',
		},
		"Address-Quick Entry": {
			"doctype": "Address",
			"layout": '[{"name": "details_section", "columns": [{"name": "column_uSSG", "fields": ["address_title", "address_type", "address_line1", "address_line2", "city", "state", "country", "pincode"]}]}]',
		},
		"CRM Call Log-Quick Entry": {
			"doctype": "CRM Call Log",
			"layout": '[{"name":"details_section","columns":[{"name":"column_uMSG","fields":["type","from","duration"]},{"name":"column_wiZT","fields":["to","status","caller","receiver"]}]}]',
		},
	}

	sidebar_fields_layouts = {
		"CRM Lead-Side Panel": {
			"doctype": "CRM Lead",
			"layout": '[{"label":"Person","name":"person_section","opened":true,"columns":[{"name":"column_XmW2","fields":["first_name","last_name","job_title_category","job_title","mobile_no","next_follow_up_on","lead_type"]}],"editingLabel":false},{"label":"Email","opened":true,"name":"section_Gmsp","columns":[{"name":"column_QpOw","fields":["email","email_status"]}],"editingLabel":false},{"label":"LinkedIn","opened":true,"name":"section_XFxG","columns":[{"name":"column_mzhO","fields":["linkedin_url","linkedin_status","linkedin_invited_by","linkedin_connected_on","last_linkedin_check"]}],"editingLabel":false},{"label":"Details","name":"details_section","opened":true,"columns":[{"name":"column_kl92","fields":["sales_campaign","organization","source","lead_score"]}]}]',
		},
		"CRM Deal-Side Panel": {
			"doctype": "CRM Deal",
			"layout": '[{"label": "Contacts", "name": "contacts_section", "opened": true, "editable": false, "contacts": []}, {"label": "Organization Details", "name": "organization_section", "opened": true, "columns": [{"name": "column_na2Q", "fields": ["organization", "website", "territory", "annual_revenue", "close_date", "probability", "next_step", "deal_owner"]}]}]',
		},
		"Contact-Side Panel": {
			"doctype": "Contact",
			"layout": '[{"label": "Details", "name": "details_section", "opened": true, "columns": [{"name": "column_eIWl", "fields": ["salutation", "first_name", "last_name", "email_id", "mobile_no", "gender", "company_name", "designation", "address"]}]}]',
		},
		"CRM Organization-Side Panel": {
			"doctype": "CRM Organization",
			"layout": '[{"label":"Details","name":"details_section","opened":true,"columns":[{"name":"column_IJOV","fields":["sales_campaign","target_market","target_industry","campaign_status","campaign_owner","start_date","end_date"]}],"showEditButton":true,"visible":8}]',
		},
  		"CRM Sales Campaign-Side Panel": {
			"doctype": "CRM Sales Campaign",
			"layout": '[{"label": "Details", "name": "details_section", "opened": true, "columns": [{"name": "column_IJOV", "fields": ["sales_campaign", "target_market", "target_industry", "campaign_status", "campaign_owner", "start_date", "end_date"]}]}]',
		},
	}

	data_fields_layouts = {
		"CRM Lead-Data Fields": {
			"doctype": "CRM Lead",
			"layout": '[{"name":"first_tab","sections":[{"label":"Communication","name":"section_QYHn","opened":true,"columns":[{"name":"column_RbBv","fields":["email","email_status","next_follow_up_on"]},{"label":"","name":"column_HgYo","fields":["linkedin_url","linkedin_status","linkedin_invited_by","linkedin_connected_on"]}],"editingLabel":false},{"label":"Details","name":"details_section","opened":true,"columns":[{"name":"column_ZgLG","fields":["sales_campaign","source"]},{"name":"column_TbYq","fields":["organization","lead_owner"]},{"name":"column_OKSX","fields":["job_title","lead_score"]}]},{"label":"Person","name":"person_section","opened":true,"columns":[{"name":"column_6c5g","fields":["first_name","gender","mobile_no"]},{"name":"column_1n7Q","fields":["last_name","lead_type","job_title_category"]}]}],"label":""}]',
		},
		"CRM Deal-Data Fields": {
			"doctype": "CRM Deal",
			"layout": '[{"label": "Details", "name": "details_section", "opened": true, "columns": [{"name": "column_z9XL", "fields": ["organization", "annual_revenue", "next_step"]}, {"name": "column_gM4w", "fields": ["website", "close_date", "deal_owner"]}, {"name": "column_gWmE", "fields": ["territory", "probability"]}]}]',
		},
	}

	for layout in quick_entry_layouts:
		if frappe.db.exists("CRM Fields Layout", layout):
			if force:
				frappe.delete_doc("CRM Fields Layout", layout)
			else:
				continue

		doc = frappe.new_doc("CRM Fields Layout")
		doc.type = "Quick Entry"
		doc.dt = quick_entry_layouts[layout]["doctype"]
		doc.layout = quick_entry_layouts[layout]["layout"]
		doc.insert()

	for layout in sidebar_fields_layouts:
		if frappe.db.exists("CRM Fields Layout", layout):
			if force:
				frappe.delete_doc("CRM Fields Layout", layout)
			else:
				continue

		doc = frappe.new_doc("CRM Fields Layout")
		doc.type = "Side Panel"
		doc.dt = sidebar_fields_layouts[layout]["doctype"]
		doc.layout = sidebar_fields_layouts[layout]["layout"]
		doc.insert()

	for layout in data_fields_layouts:
		if frappe.db.exists("CRM Fields Layout", layout):
			if force:
				frappe.delete_doc("CRM Fields Layout", layout)
			else:
				continue

		doc = frappe.new_doc("CRM Fields Layout")
		doc.type = "Data Fields"
		doc.dt = data_fields_layouts[layout]["doctype"]
		doc.layout = data_fields_layouts[layout]["layout"]
		doc.insert()


def add_property_setter():
	if not frappe.db.exists("Property Setter", {"name": "Contact-main-search_fields"}):
		doc = frappe.new_doc("Property Setter")
		doc.doctype_or_field = "DocType"
		doc.doc_type = "Contact"
		doc.property = "search_fields"
		doc.property_type = "Data"
		doc.value = "email_id"
		doc.insert()


def add_email_template_custom_fields():
	if not frappe.get_meta("Email Template").has_field("enabled"):
		click.secho("* Installing Custom Fields in Email Template")

		create_custom_fields(
			{
				"Email Template": [
					{
						"default": "0",
						"fieldname": "enabled",
						"fieldtype": "Check",
						"label": "Enabled",
						"insert_after": "",
					},
					{
						"fieldname": "reference_doctype",
						"fieldtype": "Link",
						"label": "Doctype",
						"options": "DocType",
						"insert_after": "enabled",
					},
				]
			}
		)

		frappe.clear_cache(doctype="Email Template")


def add_default_industries():
	industries = [
		"Accounting",
		"Advertising",
		"Aerospace",
		"Agriculture",
		"Airline",
		"Apparel & Accessories",
		"Automotive",
		"Banking",
		"Biotechnology",
		"Broadcasting",
		"Brokerage",
		"Chemical",
		"Computer",
		"Consulting",
		"Consumer Products",
		"Cosmetics",
		"Defense",
		"Department Stores",
		"Education",
		"Electronics",
		"Energy",
		"Entertainment & Leisure, Executive Search",
		"Financial Services",
		"Food",
		"Beverage & Tobacco",
		"Grocery",
		"Health Care",
		"Internet Publishing",
		"Investment Banking",
		"Legal",
		"Manufacturing",
		"Motion Picture & Video",
		"Music",
		"Newspaper Publishers",
		"Online Auctions",
		"Pension Funds",
		"Pharmaceuticals",
		"Private Equity",
		"Publishing",
		"Real Estate",
		"Retail & Wholesale",
		"Securities & Commodity Exchanges",
		"Service",
		"Soap & Detergent",
		"Software",
		"Sports",
		"Technology",
		"Telecommunications",
		"Television",
		"Transportation",
		"Venture Capital",
	]

	for industry in industries:
		if frappe.db.exists("CRM Industry", industry):
			continue

		doc = frappe.new_doc("CRM Industry")
		doc.industry = industry
		doc.insert()


def add_default_lead_sources():
	lead_sources = [
		"Existing Customer",
		"Reference",
		"Advertisement",
		"Cold Calling",
		"Exhibition",
		"Supplier Reference",
		"Mass Mailing",
		"Customer's Vendor",
		"Sales Campaign",
		"Walk In",
		"LinkedIn",
		"Website",
	]

	for source in lead_sources:
		if frappe.db.exists("CRM Lead Source", source):
			continue

		doc = frappe.new_doc("CRM Lead Source")
		doc.source_name = source
		doc.insert()


def add_default_lost_reasons():
	lost_reasons = [
		{
			"reason": "Pricing",
			"description": "The prospect found the pricing to be too high or not competitive.",
		},
		{"reason": "Competition", "description": "The prospect chose a competitor's product or service."},
		{
			"reason": "Budget Constraints",
			"description": "The prospect did not have the budget to proceed with the purchase.",
		},
		{
			"reason": "Missing Features",
			"description": "The prospect felt that the product or service was missing key features they needed.",
		},
		{
			"reason": "Long Sales Cycle",
			"description": "The sales process took too long, leading to loss of interest.",
		},
		{
			"reason": "No Decision-Maker",
			"description": "The prospect was not the decision-maker and could not proceed.",
		},
		{"reason": "Unresponsive Prospect", "description": "The prospect did not respond to follow-ups."},
		{"reason": "Poor Fit", "description": "The prospect was not a good fit for the product or service."},
		{"reason": "Other", "description": ""},
	]

	for reason in lost_reasons:
		if frappe.db.exists("CRM Lost Reason", reason["reason"]):
			continue

		doc = frappe.new_doc("CRM Lost Reason")
		doc.lost_reason = reason["reason"]
		doc.description = reason["description"]
		doc.insert()


def add_standard_dropdown_items():
	crm_settings = frappe.get_single("FCRM Settings")

	# don't add dropdown items if they're already present
	if crm_settings.dropdown_items:
		return

	crm_settings.dropdown_items = []

	for item in frappe.get_hooks("standard_dropdown_items"):
		crm_settings.append("dropdown_items", item)

	crm_settings.save()


def add_default_scripts():
	from crm.fcrm.doctype.fcrm_settings.fcrm_settings import create_forecasting_script

	for doctype in ["CRM Lead", "CRM Deal"]:
		create_product_details_script(doctype)
	create_forecasting_script()
