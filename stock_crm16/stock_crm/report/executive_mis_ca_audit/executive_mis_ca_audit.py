import frappe
from frappe import _
from frappe.utils import flt, getdate

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart(data)
	report_summary = get_report_summary(data)
	return columns, data, None, chart, report_summary

def get_columns():
	return [
		{"label": _("Deal ID"), "fieldname": "name", "fieldtype": "Link", "options": "Unlisted Deal Ledger", "width": 140},
		{"label": _("Date"), "fieldname": "confirmation_date", "fieldtype": "Date", "width": 110},
		{"label": _("Stock Name"), "fieldname": "stock", "fieldtype": "Link", "options": "Unlisted Stock", "width": 180},
		{"label": _("ISIN"), "fieldname": "isin_number", "fieldtype": "Data", "width": 130},
		{"label": _("Quantity"), "fieldname": "quantity", "fieldtype": "Float", "width": 100},
		{"label": _("Seller Profile"), "fieldname": "seller_profile", "fieldtype": "Link", "options": "Counterparty Profile", "width": 150},
		{"label": _("Seller Gross (₹)"), "fieldname": "seller_gross_cost", "fieldtype": "Currency", "width": 130},
		{"label": _("Buyer Profile"), "fieldname": "buyer_profile", "fieldtype": "Link", "options": "Counterparty Profile", "width": 150},
		{"label": _("Buyer Gross (₹)"), "fieldname": "buyer_gross_value", "fieldtype": "Currency", "width": 130},
		{"label": _("Stamp Duty 0.015% (₹)"), "fieldname": "stamp_duty", "fieldtype": "Currency", "width": 140},
		{"label": _("TCS 0.10% (₹)"), "fieldname": "tcs_value", "fieldtype": "Currency", "width": 130},
		{"label": _("Total Net Due (₹)"), "fieldname": "total_net_due", "fieldtype": "Currency", "width": 140},
		{"label": _("Net Arbitrage (₹)"), "fieldname": "net_arbitrage", "fieldtype": "Currency", "width": 140},
		{"label": _("Status"), "fieldname": "status_str", "fieldtype": "Data", "width": 100},
	]

def get_data(filters):
	conditions = ["docstatus != 2"]
	if filters and filters.get("from_date"):
		conditions.append(f"confirmation_date >= '{filters.get('from_date')}'")
	if filters and filters.get("to_date"):
		conditions.append(f"confirmation_date <= '{filters.get('to_date')}'")
	if filters and filters.get("docstatus_filter") == "Submitted Only":
		conditions.append("docstatus = 1")
	elif filters and filters.get("docstatus_filter") == "Draft Only":
		conditions.append("docstatus = 0")

	where_clause = "WHERE " + " AND ".join(conditions)

	deals = frappe.db.sql(f"""
		SELECT
			name, confirmation_date, stock, isin_number, quantity,
			seller_profile, seller_gross_cost,
			buyer_profile, buyer_gross_value,
			stamp_duty, tcs_value, total_net_due, net_arbitrage,
			brokerage_split, direct_expenses, seller_rate, buyer_rate, docstatus
		FROM `tabUnlisted Deal Ledger`
		{where_clause}
		ORDER BY confirmation_date DESC
	""", as_dict=True)

	for d in deals:
		d["status_str"] = "Submitted" if d.docstatus == 1 else "Draft"

	return deals

def get_chart(data):
	if not data:
		return None
	labels = [d.name for d in data[:10]]
	net_arb = [flt(d.net_arbitrage) for d in data[:10]]
	return {
		"data": {
			"labels": labels,
			"datasets": [{"name": _("Net Arbitrage Profit"), "values": net_arb}]
		},
		"type": "bar",
		"colors": ["#10b981"]
	}

def get_report_summary(data):
	if not data:
		return []

	total_volume = sum(flt(d.buyer_gross_value) for d in data)
	total_stamp = sum(flt(d.stamp_duty) for d in data)
	total_tcs = sum(flt(d.tcs_value) for d in data)
	total_arbitrage = sum(flt(d.net_arbitrage) for d in data)
	gross_spread = sum(flt(d.buyer_gross_value) - flt(d.seller_gross_cost) for d in data)

	return [
		{"value": total_volume, "label": _("Total Gross Volume"), "datatype": "Currency", "currency": "INR"},
		{"value": gross_spread, "label": _("Gross Spreads (Buy-Sell)"), "datatype": "Currency", "currency": "INR"},
		{"value": total_stamp, "label": _("Total Stamp Duty (Sec 9A)"), "datatype": "Currency", "currency": "INR"},
		{"value": total_tcs, "label": _("Total TCS (Sec 206C)"), "datatype": "Currency", "currency": "INR"},
		{"value": total_arbitrage, "label": _("Net Realized Arbitrage"), "datatype": "Currency", "currency": "INR", "indicator": "Green" if total_arbitrage >= 0 else "Red"},
	]
