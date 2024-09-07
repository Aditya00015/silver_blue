// Copyright (c) 2024, Sanskar technolab and contributors
// For license information, please see license.txt

frappe.ui.form.on("Street", {

    refresh: function (frm) {
        if (!frm.is_new()) {
            frm.set_df_property('street_name', 'read_only', 1);
            frm.set_df_property('sub_society', 'read_only', 1);
        }

    }
});
