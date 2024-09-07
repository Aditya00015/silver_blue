// Copyright (c) 2024, Sanskar technolab and contributors
// For license information, please see license.txt

frappe.ui.form.on("States", {
    refresh: function (frm) {
        frm.fields_dict['state_zone_list'].grid.wrapper.find('.grid-add-row').hide();
        if (!frm.is_new()) {
            frm.set_df_property('state_name', 'read_only', 1);
            frm.set_df_property('state_type', 'read_only', 1);
            frm.set_df_property('country_zone', 'read_only', 1);

        }
    }
    
});
