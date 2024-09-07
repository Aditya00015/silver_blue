# Copyright (c) 2024, Sanskar technolab and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DistrictZone(Document):
    def before_save(self):                                                                                                                      
        self.update_zone_wise_count()
        self.update_unique_code()

    def update_zone_wise_count(self):
        # Count the number of 'Districts' records for the specified Districts
        location_settings = frappe.get_single("Location wise Code Settings")
        
        # Retrieve the code_digit_option from the settings document
        code_digit_option = location_settings.states
        # frappe.msgprint(f"Code Digit Option: {code_digit_option}")

        # Set the `code_digit_option` field in the CountryZone doctype
        self.code_digit_option = code_digit_option
        count = frappe.db.count("District Zone", filters={"district": self.district})

        if self.code_digit_option == "Single(1)":
            # When 'Single(1)' is selected, count starts from 0 and is displayed as a single digit
            if count:
                self.zone_wise_count = str(count)  # No leading zero
            else:
                self.zone_wise_count = "1"  # Start from 0 if no records exist

        elif self.code_digit_option == "Double(01)":
            # When 'Double(01)' is selected, count starts from 01 and is displayed as two digits
            if count:
                self.zone_wise_count = str(count + 1).zfill(2)  # Format as two digits with leading zero
            else:
                self.zone_wise_count = "01"  # Start from 01 if no records exist

    def update_unique_code(self):
        # Fetch the unique code from the 'Districts' doctype
        country_code = frappe.db.get_value('Districts', self.district, 'unique_code')
        
        if country_code:
            # Concatenate the country code with the formatted count
            self.unique_code = country_code + self.zone_wise_count
        else:
            self.unique_code = self.zone_wise_count


    def after_insert(self):
        self.update_district_on_states_save()

    def update_district_on_states_save(self):
        district_zone = frappe.get_doc("Districts", {"name": self.district})


        # Check if the state already exists in the child table
        existing_state = next((row for row in district_zone.district_zone_list if row.district_zone_id == self.name), None)
            
        if not existing_state:
            # Assign the district_zone_code for the new district
            count = frappe.db.count("District Zone", filters={"district": self.district})
            new_code = count + 1
            
            # Append a new row in the district_zone_list child table of Districts
            new_row = district_zone.append("district_zone_list", {})
            new_row.district_zone_id = self.name
            new_row.district_zone_code = new_code

            # Save the Districts document
            district_zone.save(ignore_permissions=True)

            # Debug: Print the updated districts and their codes
            updated_states = [(row.district_zone_id, row.district_zone_code) for row in district_zone.district_zone_list]
            # print(f"Updated Districts after update: {updated_states}")
