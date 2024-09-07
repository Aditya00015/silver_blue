// Copyright (c) 2024, Sanskar technolab and contributors
// For license information, please see license.txt

frappe.ui.form.on("Area", {
	refresh: function (frm) {
        frm.fields_dict['area_zone_list'].grid.wrapper.find('.grid-add-row').hide();

        if (!frm.is_new()) {
            frm.set_df_property('area_name', 'read_only', 1);
            frm.set_df_property('district_zone', 'read_only', 1);
        }
    },
});
