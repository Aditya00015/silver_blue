// Copyright (c) 2024, Sanskar technolab and contributors
// For license information, please see license.txt

frappe.ui.form.on('Location wise Code Settings', {
    country_zone: function(frm) {
        // Check the selected value of 'country_zone' and set 'states_preview' accordingly
        if (frm.doc.country_zone === 'Single(1)') {
            frm.set_value('data_uink', '911');
        } else if (frm.doc.country_zone === 'Double(01)') {
            frm.set_value('data_uink', '9101');
        }
    },
    states: function(frm) {
        // Check the selected value of 'country_zone' and set 'states_preview' accordingly
        if (frm.doc.states === 'Single(1)') {
            frm.set_value('states_preview', '9111');
        } else if (frm.doc.states === 'Double(01)') {
            frm.set_value('states_preview', '91101');
        }
    },
    state_zone: function(frm) {
        // Check the selected value of 'country_zone' and set 'states_preview' accordingly
        if (frm.doc.state_zone === 'Single(1)') {
            frm.set_value('state_zone_preview', '91111');
        } else if (frm.doc.state_zone === 'Double(01)') {
            frm.set_value('state_zone_preview', '911101');
        }
    },
    districts: function(frm) {
        // Check the selected value of 'country_zone' and set 'states_preview' accordingly
        if (frm.doc.districts === 'Single(1)') {
            frm.set_value('districts_preview', '911111');
        } else if (frm.doc.districts === 'Double(01)') {
            frm.set_value('districts_preview', '9111101');
        }
    },
    district_zone: function(frm) {
        // Check the selected value of 'country_zone' and set 'states_preview' accordingly
        if (frm.doc.district_zone === 'Single(1)') {
            frm.set_value('districts_zone_preview', '9111111');
        } else if (frm.doc.district_zone === 'Double(01)') {
            frm.set_value('districts_zone_preview', '91111101');
        }
    },
    area: function(frm) {
        // Check the selected value of 'country_zone' and set 'states_preview' accordingly
        if (frm.doc.area === 'Single(1)') {
            frm.set_value('districts_zone_preview____copy', '91111111');
        } else if (frm.doc.area === 'Double(01)') {
            frm.set_value('districts_zone_preview____copy', '911111101');
        }
    },
    area_zone: function(frm) {
        // Check the selected value of 'country_zone' and set 'states_preview' accordingly
        if (frm.doc.area === 'Single(1)') {
            frm.set_value('area_zone_preview', '911111111');
        } else if (frm.doc.area === 'Double(01)') {
            frm.set_value('area_zone_preview', '9111111101');
        }
    },
    society: function(frm) {
        // Check the selected value of 'country_zone' and set 'states_preview' accordingly
        if (frm.doc.society === 'Single(1)') {
            frm.set_value('society_preview', '9111111111');
        } else if (frm.doc.society === 'Double(01)') {
            frm.set_value('society_preview', '91111111101');
        }
    },
    sub_society: function(frm) {
        // Check the selected value of 'country_zone' and set 'states_preview' accordingly
        if (frm.doc.sub_society === 'Single(1)') {
            frm.set_value('sub_society_preview', '91111111111');
        } else if (frm.doc.sub_society === 'Double(01)') {
            frm.set_value('sub_society_preview', '911111111101');
        }
    },

    street: function(frm) {
        // Check the selected value of 'country_zone' and set 'states_preview' accordingly
        if (frm.doc.street === 'Single(1)') {
            frm.set_value('street_preview', '911111111111');
        } else if (frm.doc.street === 'Double(01)') {
            frm.set_value('street_preview', '9111111111101');
        }
    },
});
