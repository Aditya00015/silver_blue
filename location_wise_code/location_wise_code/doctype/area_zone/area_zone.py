# Copyright (c) 2024, Sanskar technolab and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AreaZone(Document):
    def before_save(self):
        # Update the state count and unique code before saving
        self.update_state_count()
        self.update_unique_code()
        # frappe.msgprint(f"State Wise Count in before_save: {self.zone_wise_count}")

    def update_state_count(self):
        # Query to get the count of records for the current area
        location_settings = frappe.get_single("Location wise Code Settings")
        
        # Retrieve the code_digit_option from the settings document
        code_digit_option = location_settings.states
        # frappe.msgprint(f"Code Digit Option: {code_digit_option}")

        # Set the `code_digit_option` field in the CountryZone doctype
        self.code_digit_option = code_digit_option
        count = frappe.db.count("Area Zone", filters={"area": self.area}) + 1  # Always add 1 to the count

        if self.code_digit_option == "Single(1)":
            # When 'Single(1)' is selected, display the count as a single digit
            self.zone_wise_count = str(count)  # No leading zero, starts from 1

        elif self.code_digit_option == "Double(01)":
            # When 'Double(01)' is selected, display the count as two digits with leading zeros
            self.zone_wise_count = str(count).zfill(2)  # Format as two digits with leading zero

  

    def update_unique_code(self):
        # Fetch the custom country code from the 'Country' doctype
        country_code = frappe.db.get_value('Area', self.area, 'unique_code')
        
        if country_code:
            # Concatenate the country code with the formatted count
            self.unique_code = country_code + self.zone_wise_count
        else:
            self.unique_code = self.zone_wise_count
    def after_insert(self):
        self.update_district_on_states_save()

    def update_district_on_states_save(self):
        area_zone = frappe.get_doc("Area", {"name": self.area})
       

        # Check if the state already exists in the child table
        existing_state = next((row for row in area_zone.area_zone_list if row.area_zone_id == self.name), None)
            
        if not existing_state:
            # Assign the area_wise_code for the new district
            count = frappe.db.count("Area Zone", filters={"area": self.area})
            new_code = count + 1
            
            # Append a new row in the area_zone_list child table of Districts
            new_row = area_zone.append("area_zone_list", {})
            new_row.area_zone_id = self.name
            new_row.zone_code = new_code

            # Save the Districts document
            area_zone.save(ignore_permissions=True)

            # Debug: Print the updated districts and their codes
            updated_states = [(row.area_zone_id, row.zone_code) for row in area_zone.area_zone_list]
            # print(f"Updated Districts after update: {updated_states}")


