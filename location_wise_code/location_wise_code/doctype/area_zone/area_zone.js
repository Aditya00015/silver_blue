// Copyright (c) 2024, Sanskar technolab and contributors
// For license information, please see license.txt

frappe.ui.form.on("Area Zone", {
	refresh: function (frm) {
        frm.fields_dict['society_list'].grid.wrapper.find('.grid-add-row').hide();

        if (!frm.is_new()) {
            frm.set_df_property('zone_name', 'read_only', 1);
            frm.set_df_property('area', 'read_only', 1);

        }
    },
 
});
