app_name = "stock_crm16"
app_title = "Stock CRM 16"
app_publisher = "Off Market Venture"
app_description = "Share Market & Unlisted Equity CRM for Frappe Framework & ERPNext v16"
app_email = "admin@offmarketventure.com"
app_license = "mit"

# Includes in <head>
# ------------------

# Document Events
# ---------------
# Hook on_submit for Unlisted Deal Ledger to trigger audit logs or WhatsApp notifications
doc_events = {
	"Unlisted Deal Ledger": {
		"on_submit": "stock_crm16.stock_crm.doctype.unlisted_deal_ledger.unlisted_deal_ledger.on_submit_deal",
	}
}

# Required Apps
required_apps = ["frappe", "erpnext"]
