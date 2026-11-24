
"""
ContactVault - Contact Services

This module contains the business logic for
adding, deleting, searching, updating and
listing contacts.
"""

from contact_manager.models import Contact


# ==========================================
# 1. CONTACT SERVICE CLASS
# ==========================================

class ContactService:
    """
    Manages contact records using dictionary storage.

    Contacts are stored using their unique IDs
    as dictionary keys.
    """

    def __init__(self):
        """Initialize an empty contact collection."""

        self._contacts: dict[str, Contact] = {}


    # ======================================
    # 2. CHECK FOR DUPLICATE INFORMATION
    # ======================================

    def _check_duplicates(
        self,
        email: str,
        phone: str,
        exclude_id: str | None = None
    ):
        """
        Prevent duplicate email addresses and phone numbers.

        Args:
            email: Email to check.
            phone: Phone number to check.
            exclude_id: Contact ID to exclude during updates.

        Raises:
            ValueError: If email or phone already exists.
        """

        for contact in self._contacts.values():

            if contact.id == exclude_id:
                continue

            if contact.email.lower() == email.lower():

                raise ValueError(
                    "A contact with this email already exists."
                )

            if contact.phone == phone:

                raise ValueError(
                    "A contact with this phone number already exists."
                )


    # ======================================
    # 3. ADD CONTACT
    # ======================================

    def add_contact(self, contact: Contact) -> Contact:
        """
        Add a new contact to the collection.

        Args:
            contact: Contact object to add.

        Returns:
            The newly added Contact object.

        Raises:
            TypeError: If the supplied object is not a Contact.
            ValueError: If a duplicate contact exists.
        """

        if not isinstance(contact, Contact):

            raise TypeError(
                "Expected a Contact object."
            )

        if contact.id in self._contacts:

            raise ValueError(
                "A contact with this ID already exists."
            )

        self._check_duplicates(
            contact.email,
            contact.phone
        )

        self._contacts[contact.id] = contact

        return contact


    # ======================================
    # 4. DELETE CONTACT
    # ======================================

    def delete_contact(self, contact_id: str) -> bool:
        """
        Delete a contact using its unique ID.

        Args:
            contact_id: Unique contact identifier.

        Returns:
            True if deleted, otherwise False.
        """

        if not isinstance(contact_id, str):
            return False

        return self._contacts.pop(contact_id, None) is not None


    # ======================================
    # 5. GET CONTACT BY ID
    # ======================================

    def get_contact(self, contact_id: str) -> Contact | None:
        """
        Retrieve a contact using its unique ID.

        Args:
            contact_id: Unique contact identifier.

        Returns:
            Contact object if found, otherwise None.
        """

        if not isinstance(contact_id, str):
            return None

        return self._contacts.get(contact_id)


    # ======================================
    # 6. SEARCH CONTACTS
    # ======================================

    def search_contacts(self, query: str) -> list[Contact]:
        """
        Search contacts by name, email or phone number.

        The search is case-insensitive.

        Args:
            query: Search keyword.

        Returns:
            A list of matching contacts.
        """

        if not isinstance(query, str):
            raise TypeError(
                "Search query must be a string."
            )

        query = query.strip().lower()

        if not query:
            return []

        # Remove non-digits for phone matching
        phone_query = "".join(
            character for character in query
            if character.isdigit()
        )

        results = []

        for contact in self._contacts.values():

            matches_text = (
                query in contact.name.lower()
                or query in contact.email.lower()
            )

            matches_phone = (
                bool(phone_query)
                and phone_query in "".join(
                    character for character in contact.phone
                    if character.isdigit()
                )
            )

            if matches_text or matches_phone:

                results.append(contact)

        return sorted(
            results,
            key=lambda contact: contact.name.lower()
        )


    # ======================================
    # 7. GET ALL CONTACTS
    # ======================================

    def get_all_contacts(self) -> list[Contact]:
        """
        Return all contacts alphabetically by name.

        Returns:
            A list of Contact objects.
        """

        return sorted(
            self._contacts.values(),
            key=lambda contact: contact.name.lower()
        )


    # ======================================
    # 8. UPDATE CONTACT
    # ======================================

    def update_contact(
        self,
        contact_id: str,
        **kwargs
    ) -> Contact | None:
        """
        Update an existing contact.

        The update is validated before replacing
        the original contact.

        Args:
            contact_id: ID of the contact.
            **kwargs: Fields to update.

        Returns:
            Updated Contact object or None if not found.
        """
        allowed_fields = {
            "name",
            "email",
            "phone",
            "address"
        }

        invalid_fields = set(kwargs) - allowed_fields

        if invalid_fields:
            raise ValueError(
                f"Unsupported fields: {', '.join(sorted(invalid_fields))}"
            )

        existing_contact = self.get_contact(contact_id)

        if existing_contact is None:
            return None

        # Create a candidate using existing data
        updated_data = existing_contact.to_dict()

        updated_data.update(kwargs)

        # Reconstructing validates all updated values
        updated_contact = Contact.from_dict(updated_data)

        # Check duplicates while excluding this contact
        self._check_duplicates(
            updated_contact.email,
            updated_contact.phone,
            exclude_id=contact_id
        )

        # Replace the original only after all checks pass
        self._contacts[contact_id] = updated_contact

        return updated_contact


    # ======================================
    # 9. CONTACT COUNT
    # ======================================

    def get_contact_count(self) -> int:
        """
        Return the total number of saved contacts.
        """

        return len(self._contacts)
