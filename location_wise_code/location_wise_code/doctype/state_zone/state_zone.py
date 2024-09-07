# Copyright (c) 2024, Sanskar technolab and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class StateZone(Document):

    def before_save(self):
        self.update_zone_wise_count()
        self.update_unique_code()

    def update_zone_wise_count(self):
        # Count the number of 'State Zone' records for the specified state
        location_settings = frappe.get_single("Location wise Code Settings")
        
        # Retrieve the code_digit_option from the settings document
        code_digit_option = location_settings.states
    

        # Set the `code_digit_option` field in the CountryZone doctype
        self.code_digit_option = code_digit_option
        count = frappe.db.count("State Zone", filters={"state": self.state}) + 1  # Always add 1 to the count

        if self.code_digit_option == "Single(1)":
            # When 'Single(1)' is selected, display the count as a single digit
            self.zone_wise_count = str(count)  # No leading zero, starts from 1

        elif self.code_digit_option == "Double(01)":
            # When 'Double(01)' is selected, display the count as two digits with leading zeros
            self.zone_wise_count = str(count).zfill(2)  # Format as two digits with leading zero

    def update_unique_code(self):
        country_code = frappe.db.get_value("States", self.state, "unique_code")

        if country_code:
            self.unique_code = country_code + str(self.zone_wise_count)
        else:
            self.unique_code = str(self.zone_wise_count)

    def after_insert(self):
        self.update_state_zone_on_states_save()

    def update_state_zone_on_states_save(self):
        state_zone = frappe.get_doc("States", {"name": self.state})


        # existing_states = [(row.state_name, row.state_code) for row in state_zone.state_zone_list]
        # print(f"Existing States before update: {existing_states}")

            # Check if the state already exists in the child table
        existing_state = next((row for row in state_zone.state_zone_list if row.state_zone_id == self.name), None)
            
        if not existing_state:
                # Assign the state_code for new state
                count = frappe.db.count("State Zone", filters={"state": self.state})
                new_code = count + 1
                
                # Append a new row in the state_zone_code child table of Country Zone
                new_row = state_zone.append("state_zone_list", {})
                new_row.state_zone_id = self.name
                new_row.state_zone_code = new_code

                # Save the Country Zone document
                state_zone.save(ignore_permissions=True)    

                # Debug: Print the updated states and their codes
                updated_states = [(row.state_zone_id, row.state_zone_code) for row in state_zone.state_zone_list]
                # print(f"Updated States after update: {updated_states}")

