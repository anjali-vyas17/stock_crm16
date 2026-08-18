// Copyright (c) 2026, Anjali and contributors
// For license information, please see license.txt

frappe.ui.form.on('Unlisted Stock', {
	on_submit: function(frm) {
		frappe.show_alert({
			message: __('Unlisted Stock submitted successfully! Redirecting to Counterparty Profile...'),
			indicator: 'green'
		});

		// Redirect to create a new Counterparty Profile (which contains Counterparty Bank Accounts)
		setTimeout(function() {
			frappe.new_doc('Counterparty Profile');
		}, 500);
	}
});
