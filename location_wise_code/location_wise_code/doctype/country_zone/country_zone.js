


frappe.ui.form.on("Country Zone", {
    refresh: function (frm) {
        frm.fields_dict['states_list'].grid.wrapper.find('.grid-add-row').hide();

        if (!frm.is_new()) {
            frm.set_df_property('zone_name', 'read_only', 1);

       
            frm.set_df_property('country', 'read_only', 1);
        }
        
    },

    
    // This function will be triggered when the form is loaded or field values are changed

    // onload: function(frm) {
       
    //     frappe.call({
    //         method: "frappe.client.get_list",
    //         args: {	
    //             doctype: "States",
    //             filters: { "zone_name": frm.doc.zone_name },
    //             fields: ["name", "state_name", "state_wise_count"],  // Adjust fields as per your needs
    //             limit_page_length: 0 
    //         },
    //         callback: function(response) {	
    //             if (response.message) {
    //                 console.log(response.message ); //
    //                 // Clear existing rows in the child table   
    //                 frm.clear_table("states_list");

    //                 // Use a Set to keep track of added zones
    //                 let addedZones = new Set();

    //                // Sort the response data in ascending order by state_wise_count (zone_code)
	// 			   let sortedZones = response.message.sort((a, b) => a.state_wise_count - b.state_wise_count);

	// 			   // Loop through the sorted Country Zone records and add them to the child table if not already added
	// 			   sortedZones.forEach(function(zone) {
	// 				   if (!addedZones.has(zone.name)) {
	// 					   let row = frm.add_child("states_list");
	// 					   row.state_name = zone.name;
	// 					   row.state_code = zone.state_wise_count;  // Assign additional fields if needed
	// 					   addedZones.add(zone.name);  // Mark this zone as added
	// 				   }
	// 			   });
    //                 // Refresh the field to update the UI
    //                 frm.refresh_field("states_list");
	// 				frm.save();
    //             }
    //         }
    //     });
    // },
});