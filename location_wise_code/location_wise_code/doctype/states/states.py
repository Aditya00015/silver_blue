import frappe
from frappe.model.document import Document

class States(Document):
    def before_save(self):
        # Update the state count and unique code before saving
        self.update_state_count()
        self.update_unique_code() 
        
    def update_state_count(self):
        location_settings = frappe.get_single("Location wise Code Settings")
        
        # Retrieve the code_digit_option from the settings document
        code_digit_option = location_settings.states
       

        # Set the `code_digit_option` field in the CountryZone doctype
        self.code_digit_option = code_digit_option

        # Query to get the count of records for the current country and zone name
        count = frappe.db.count("States", filters={"zone_name": self.zone_name, "country": self.country}) + 1  # Always add 1 to the count

        if self.code_digit_option == "Single(1)":
            # When 'Single(1)' is selected, display the count as a single digit
            self.state_wise_count = str(count)  # No leading zero, starts from 1

        elif self.code_digit_option == "Double(01)":
            # When 'Double(01)' is selected, display the count as two digits with leading zeros
            self.state_wise_count = str(count).zfill(2)  # Format as two digits with leading zero


    def update_unique_code(self):
        # Fetch the unique code from the Country Zone
        unique_code = frappe.db.get_value('Country Zone', self.country_zone, 'unique_code')

        # Concatenate the unique code with state_wise_count
        self.unique_code = unique_code + str(self.state_wise_count) if unique_code else str(self.state_wise_count)

    def after_insert(self):
        # Validate method is called before saving; update the Country Zone as needed
        # print("Validating State")
        self.update_country_zone_on_states_save()

    def update_country_zone_on_states_save(self):
        # Fetch the corresponding Country Zone based on the state
        country_zone = frappe.get_doc("Country Zone", {"name": self.country_zone})
        if not country_zone:
            # frappe.msgprint(f"Country Zone with state_name {self.state_name} not found.")
            return

        # Debug: Print existing states and their codes
        existing_states = [(row.state_name, row.state_code) for row in country_zone.states_list]
        # print(f"Existing States before update: {existing_states}")

        # Check if the state already exists in the child table
        existing_state = next((row for row in country_zone.states_list if row.state_id == self.name), None)
        
        if not existing_state:
            # Assign the state_code for new state
            count = frappe.db.count("States", filters={"zone_name": self.zone_name, "country": self.country})
            new_code = count + 1
            
            # Append a new row in the states_list child table of Country Zone
            new_row = country_zone.append("states_list", {})
            new_row.state_id = self.name
            new_row.state_code = new_code

            # Save the Country Zone document
            country_zone.save(ignore_permissions=True)

            # Debug: Print the updated states and their codes
            updated_states = [(row.state_id, row.state_code) for row in country_zone.states_list]
            # print(f"Updated States after update: {updated_states}")