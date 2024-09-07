

frappe.ui.form.on("Country", {
    refresh: function (frm) {
        frm.fields_dict['custom_country_zone_list'].grid.wrapper.find('.grid-add-row').hide();
    }
});
    