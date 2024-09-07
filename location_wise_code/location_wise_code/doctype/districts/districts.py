# Copyright (c) 2024, Sanskar technolab and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Districts(Document):
    def before_save(self):                                                                                                                      
        self.update_district_wise_count()
        self.update_unique_code()

    def update_district_wise_count(self):
        # Count the number of 'Districts' records for the specified state zone
        location_settings = frappe.get_single("Location wise Code Settings")
        
        # Retrieve the code_digit_option from the settings document
        code_digit_option = location_settings.states
        

        # Set the `code_digit_option` field in the CountryZone doctype
        self.code_digit_option = code_digit_option
        count = frappe.db.count("Districts", filters={"state_zone": self.state_zone}) + 1  # Always add 1 to the count

        if self.code_digit_option == "Single(1)":
            # When 'Single(1)' is selected, display the count as a single digit
            self.district_wise_count = str(count)  # No leading zero, starts from 1

        elif self.code_digit_option == "Double(01)":
            # When 'Double(01)' is selected, display the count as two digits with leading zeros
            self.district_wise_count = str(count).zfill(2)  # Format as two digits with leading zero


    def update_unique_code(self):
        # Fetch the unique code from the 'State Zone' doctype
        country_code = frappe.db.get_value('State Zone', self.state_zone, 'unique_code')
        
        if country_code:
            # Concatenate the country code with the formatted count
            self.unique_code = country_code + self.district_wise_count
        else:
            self.unique_code = self.district_wise_count

    def after_insert(self):
        self.update_district_on_states_save()
        
    def update_district_on_states_save(self):
        district = frappe.get_doc("State Zone", {"name": self.state_zone})
       

        # Check if the state already exists in the child table
        existing_state = next((row for row in district.district_list if row.district_id == self.district_name), None)
            
        if not existing_state:
            # Assign the district_code for the new district
            count = frappe.db.count("Districts", filters={"state_zone": self.state_zone})
            new_code = count + 1
            
            # Append a new row in the district_list child table of State Zone
            new_row = district.append("district_list", {})
            new_row.district_id = self.name
            new_row.district_code = new_code

            # Save the State Zone document
            district.save(ignore_permissions=True)

            # Debug: Print the updated districts and their codes
            updated_states = [(row.district_id, row.district_code) for row in district.district_list]
            # print(f"Updated Districts after update: {updated_states}")