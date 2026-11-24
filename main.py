
"""
ContactVault - Main Application

Interactive command-line contact management system.

Features:
    - Add contacts
    - View contacts
    - Search contacts
    - Update contacts
    - Delete contacts
    - JSON persistence
"""

from contact_manager import (
    Contact,
    ContactService,
    ContactStorage
)


# ==========================================
# 1. APPLICATION DISPLAY
# ==========================================

def display_header():
    """Display the application heading."""

    print("\n" + "=" * 55)
    print("              CONTACTVAULT")
    print("          Contact Management System")
    print("=" * 55)


def display_menu():
    """Display the available menu operations."""

    print("\nMAIN MENU")
    print("-" * 35)
    print("1. Add Contact")
    print("2. View All Contacts")
    print("3. Search Contact")
    print("4. Update Contact")
    print("5. Delete Contact")
    print("6. Exit")
    print("-" * 35)


# ==========================================
# 2. DISPLAY CONTACT INFORMATION
# ==========================================

def display_contact(contact, number=None):
    """Display an individual contact."""

    prefix = f"[{number}] " if number is not None else ""

    print(f"\n{prefix}{contact.name}")
    print("-" * 35)
    print(f"Email   : {contact.email}")
    print(f"Phone   : {contact.phone}")
    print(f"Address : {contact.address or 'Not provided'}")
    print(f"ID      : {contact.id[:8]}")


def display_contacts(contacts):
    """Display a collection of contacts."""

    if not contacts:
        print("\nNo contacts found.")
        return

    print(f"\nTOTAL CONTACTS: {len(contacts)}")

    print("-" * 45)

    for index, contact in enumerate(contacts, start=1):

        display_contact(contact, index)

    print("\n" + "-" * 45)


# ==========================================
# 3. SAVE APPLICATION DATA
# ==========================================

def save_data(service, storage):
    """Save all current contacts to JSON storage."""

    try:

        storage.save_contacts(
            service.get_all_contacts()
        )

        return True

    except OSError as error:

        print(f"\nStorage error: {error}")

        return False


# ==========================================
# 4. ADD CONTACT
# ==========================================

def add_contact(service, storage):
    """Collect details and add a new contact."""

    print("\n--- ADD NEW CONTACT ---")

    try:

        name = input("Enter name: ").strip()

        email = input("Enter email: ").strip()

        phone = input("Enter phone number: ").strip()

        address = input("Enter address (optional): ").strip()


        contact = Contact(
            name=name,
            email=email,
            phone=phone,
            address=address
        )


        service.add_contact(contact)

        if save_data(service, storage):

            print("\nContact added successfully!")

            print(f"Contact ID: {contact.id[:8]}")

        else:

            # Roll back in-memory change if persistence fails
            service.delete_contact(contact.id)

            print("Contact was not saved. Please try again.")

    except (ValueError, TypeError) as error:

        print(f"\nUnable to add contact: {error}")


# ==========================================
# 5. VIEW CONTACTS
# ==========================================

def view_contacts(service):
    """Display every saved contact."""

    print("\n--- ALL CONTACTS ---")

    contacts = service.get_all_contacts()

    display_contacts(contacts)


# ==========================================
# 6. SEARCH CONTACT
# ==========================================

def search_contact(service):
    """Search contacts by name, email or phone."""

    print("\n--- SEARCH CONTACT ---")

    query = input(
        "Enter name, email or phone to search: "
    ).strip()

    if not query:

        print("\nSearch query cannot be empty.")

        return

    results = service.search_contacts(query)

    print(f"\nSEARCH RESULTS: {len(results)}")

    display_contacts(results)


# ==========================================
# 7. SELECT CONTACT
# ==========================================

def select_contact(service):
    """Allow the user to select a contact by list number."""

    contacts = service.get_all_contacts()

    if not contacts:

        print("\nNo contacts available.")

        return None

    display_contacts(contacts)

    choice = input(
    "\nEnter the list number shown in brackets (e.g. 1): "
).strip()

    try:

        index = int(choice) - 1

    except ValueError:

        print("\nPlease enter a valid number.")

        return None


    if index < 0 or index >= len(contacts):

        print("\nInvalid contact selection.")

        return None

    return contacts[index]


# ==========================================
# 8. UPDATE CONTACT
# ==========================================

def update_contact(service, storage):
    """Update selected contact information."""

    print("\n--- UPDATE CONTACT ---")

    contact = select_contact(service)

    if contact is None:
        return

    print("\nPress Enter to keep the existing value.")

    print("For address only, enter '-' to clear it.")


    name = input(
        f"Name [{contact.name}]: "
    ).strip()

    email = input(
        f"Email [{contact.email}]: "
    ).strip()

    phone = input(
        f"Phone [{contact.phone}]: "
    ).strip()

    address = input(
        f"Address [{contact.address}]: "
    ).strip()


    updates = {}


    if name:
        updates["name"] = name

    if email:
        updates["email"] = email

    if phone:
        updates["phone"] = phone

    if address == "-":
        updates["address"] = ""

    elif address:
        updates["address"] = address


    if not updates:

        print("\nNo changes were provided.")

        return


    # Save original data for rollback if storage fails
    original = contact.to_dict()

    try:

        updated = service.update_contact(
            contact.id,
            **updates
        )

        if updated is None:

            print("\nContact no longer exists.")

            return


        if save_data(service, storage):

            print("\nContact updated successfully!")

        else:

            # Restore the original contact if saving fails
            service.update_contact(
                contact.id,
                name=original["name"],
                email=original["email"],
                phone=original["phone"],
                address=original["address"]
            )

            print("Changes were not saved.")

    except (ValueError, TypeError) as error:

        print(f"\nUnable to update contact: {error}")


# ==========================================
# 9. DELETE CONTACT
# ==========================================

def delete_contact(service, storage):
    """Delete a selected contact after confirmation."""

    print("\n--- DELETE CONTACT ---")

    contact = select_contact(service)

    if contact is None:
        return


    confirmation = input(
        f"\nDelete {contact.name}? (yes/no): "
    ).strip().lower()


    if confirmation not in {"yes", "y"}:

        print("\nDeletion cancelled.")

        return


    deleted = service.delete_contact(contact.id)

    if not deleted:

        print("\nUnable to find this contact.")

        return


    if save_data(service, storage):

        print("\nContact deleted successfully!")

    else:

        # Restore in-memory contact if persistence fails
        service.add_contact(contact)

        print("Deletion could not be saved.")


# ==========================================
# 10. LOAD SAVED CONTACTS
# ==========================================

def load_existing_contacts(service, storage):
    """Restore saved contacts when the application starts."""

    contacts = storage.load_contacts()

    for contact in contacts:

        service.add_contact(contact)

    return len(contacts)


# ==========================================
# 11. MAIN APPLICATION
# ==========================================

def main():
    """Initialize and run ContactVault."""

    service = ContactService()

    storage = ContactStorage()


    try:

        restored_count = load_existing_contacts(
            service,
            storage
        )

    except (OSError, ValueError, TypeError) as error:

        print(f"\nUnable to load contact database: {error}")

        print("Please inspect the storage file before continuing.")

        return 1


    display_header()

    print(
        f"\nRestored contacts: {restored_count}"
    )


    actions = {

        "1": lambda: add_contact(service, storage),

        "2": lambda: view_contacts(service),

        "3": lambda: search_contact(service),

        "4": lambda: update_contact(service, storage),

        "5": lambda: delete_contact(service, storage)

    }


    try:

        while True:

            display_menu()

            choice = input(
                "\nSelect an option (1-6): "
            ).strip()


            if choice == "6":

                print("\nThank you for using ContactVault!")

                print("Your saved contacts are safe.")

                break


            action = actions.get(choice)

            if action is None:

                print("\nInvalid choice. Please select 1-6.")

                continue


            action()


    except (KeyboardInterrupt, EOFError):

        print("\n\nApplication closed.")

    return 0


# ==========================================
# 12. APPLICATION ENTRY POINT
# ==========================================

if __name__ == "__main__":

    raise SystemExit(main())
