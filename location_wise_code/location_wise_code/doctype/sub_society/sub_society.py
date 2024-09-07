# Copyright (c) 2024, Sanskar technolab and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SubSociety(Document):
    def before_save(self):                                                                                                                      
        self.update_sub_society_wise_count()
        self.update_unique_code()

    def update_sub_society_wise_count(self):
        # Count the number of 'Sub Society' records for the specified society
        location_settings = frappe.get_single("Location wise Code Settings")
        
        # Retrieve the code_digit_option from the settings document
        code_digit_option = location_settings.states
        # frappe.msgprint(f"Code Digit Option: {code_digit_option}")

        # Set the `code_digit_option` field in the CountryZone doctype
        self.code_digit_option = code_digit_option
        location_settings = frappe.get_single("Location wise Code Settings")
        
        # Retrieve the code_digit_option from the settings document
        code_digit_option = location_settings.states
        # frappe.msgprint(f"Code Digit Option: {code_digit_option}")

        # Set the `code_digit_option` field in the CountryZone doctype
        self.code_digit_option = code_digit_option
        count = frappe.db.count("Sub Society", filters={"society": self.society}) + 1  # Always add 1 to start count from 1

        if self.code_digit_option == "Single(1)":
            # When 'Single(1)' is selected, display the count as a single digit
            self.sub_society_wise_count = str(count)  # No leading zero

        elif self.code_digit_option == "Double(01)":
            # When 'Double(01)' is selected, display the count as two digits with leading zeros
            self.sub_society_wise_count = str(count).zfill(2)  # Format as two digits with leading zero


    def update_unique_code(self):
        # Fetch the custom country code from the 'Country' doctype
        country_code = frappe.db.get_value('Society', self.society, 'unique_code')
        
        if country_code:
            # Concatenate the country code with the formatted count
            self.unique_code = country_code + self.sub_society_wise_count
        else:
            self.unique_code = self.sub_society_wise_count


    def after_insert(self):
        self.update_district_on_states_save()

    def update_district_on_states_save(self):
        society = frappe.get_doc("Society", {"name": self.society})
       

        # Check if the state already exists in the child table
        existing_state = next((row for row in society.sub_society_list if row.sub_society_id == self.name), None)
            
        if not existing_state:
            # Assign the area_wise_code for the new district
            count = frappe.db.count("Sub Society", filters={"society": self.society})
            new_code = count + 1
            
            # Append a new row in the sub_society_list child table of Districts
            new_row = society.append("sub_society_list", {})
            new_row.sub_society_id = self.name
            new_row.sub_society_code = new_code

            # Save the Districts document
            society.save(ignore_permissions=True)

            # Debug: Print the updated districts and their codes
            updated_states = [(row.sub_society_id, row.sub_society_code) for row in society.sub_society_list]
            # print(f"Updated Districts after update: {updated_states}")
