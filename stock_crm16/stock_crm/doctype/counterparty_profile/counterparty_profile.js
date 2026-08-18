// Copyright (c) 2026, Anjali and contributors
// For license information, please see license.txt

frappe.ui.form.on('Counterparty Profile', {
	on_submit: function(frm) {
		frappe.show_alert({
			message: __('Counterparty Profile submitted successfully! Redirecting to Unlisted Deal Ledger...'),
			indicator: 'green'
		});

		// Redirect to create a new Unlisted Deal Ledger record
		setTimeout(function() {
			frappe.new_doc('Unlisted Deal Ledger');
		}, 500);
	}
});
