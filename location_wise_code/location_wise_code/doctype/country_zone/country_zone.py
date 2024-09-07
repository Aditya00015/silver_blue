# Copyright (c) 2024, Sanskar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CountryZone(Document):
    def before_save(self):
        self.update_country_wise_count()
        self.update_unique_code()

    def update_country_wise_count(self):
        # Fetch the single document from the 'Location wise Code Settings' doctype
        location_settings = frappe.get_single("Location wise Code Settings")
        
        # Retrieve the code_digit_option from the settings document
        code_digit_option = location_settings.country_zone
        

        # Set the `code_digit_option` field in the CountryZone doctype
        self.code_digit_option = code_digit_option

        # Count the number of 'Country Zone' records for the specified country
        count = (
            frappe.db.count("Country Zone", filters={"country": self.country}) + 1
        )  # Always add 1 to the count

        if code_digit_option == "Single(1)":
            # When 'Single(1)' is selected, display the count as a single digit
            self.country_wise_count = str(count)  # No leading zero, starts from 1

        elif code_digit_option == "Double(01)":
            # When 'Double(01)' is selected, display the count as two digits with leading zeros
            self.country_wise_count = str(count).zfill(
                2
            )  # Format as two digits with leading zero

    

    def update_unique_code(self):
        # Fetch the custom country code from the 'Country' doctype
        country_code = frappe.db.get_value(
            "Country", self.country, "custom_country_code"
        )

        if country_code:
            # Concatenate the country code with the formatted count
            self.unique_code = country_code + self.country_wise_count
        else:
            self.unique_code = self.country_wise_count


    def after_insert(self):
        self.update_district_on_states_save()

    def update_district_on_states_save(self):
        # Fetch the country document using its name
        country = frappe.get_doc("Country", {"name": self.country})
        # frappe.msgprint(f"Processing country: {country.name}")

        # Check if the state already exists in the child table
        existing_state = next((row for row in country.custom_country_zone_list if row.country_zone == self.name), None)

        if not existing_state:
            # Assign a new area_wise_code for the new district
            count = frappe.db.count("Country Zone", filters={"country": self.country})
            new_code = count + 1

            # Append a new row in the custom_country_zone_list child table of Districts
            new_row = country.append("custom_country_zone_list", {})
            new_row.country_zone = self.name
            new_row.zone_code = new_code

            # Save the updated Country document
            country.save(ignore_permissions=True)

            # Debug: Print the updated districts and their codes
            updated_states = [(row.country_zone, row.zone_code) for row in country.custom_country_zone_list]
            # frappe.msgprint(f"Updated Districts after update: {updated_states}")

