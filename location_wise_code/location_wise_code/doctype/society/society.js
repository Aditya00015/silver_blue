// Copyright (c) 2024, Sanskar technolab and contributors
// For license information, please see license.txt

frappe.ui.form.on("Society", {
	refresh: function (frm) {
        frm.fields_dict['sub_society_list'].grid.wrapper.find('.grid-add-row').hide();

        if (!frm.is_new()) {
            frm.set_df_property('society_name', 'read_only', 1);
            frm.set_df_property('area_zone', 'read_only', 1);
        }
    },
   
}); 
