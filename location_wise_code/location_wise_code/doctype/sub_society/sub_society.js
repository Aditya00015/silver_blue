// Copyright (c) 2024, Sanskar technolab and contributors
// For license information, please see license.txt
frappe.ui.form.on("Sub Society", {
    refresh: function (frm) {
        // Hide the 'Add Row' button for street_list child table
        frm.fields_dict['street_list'].grid.wrapper.find('.grid-add-row').hide();
        
    
        if (!frm.is_new()) {
            frm.set_df_property('sub_society_name', 'read_only', 1);
            frm.set_df_property('society', 'read_only', 1);
        }
    }
});
