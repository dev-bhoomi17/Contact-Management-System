
"""
ContactVault - JSON Storage

This module handles saving and loading contact
records using JSON file persistence.
"""

import json

from pathlib import Path

from contact_manager.models import Contact


# ==========================================
# 1. STORAGE CONFIGURATION
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIRECTORY = PROJECT_ROOT / "data"

DEFAULT_STORAGE_FILE = DATA_DIRECTORY / "contacts.json"


# ==========================================
# 2. CONTACT STORAGE CLASS
# ==========================================

class ContactStorage:
    """
    Provides JSON-based persistence for contacts.

    Contact objects are serialized into JSON dictionaries
    and reconstructed when the application starts.
    """

    def __init__(self, file_path=None):

        self.file_path = Path(
            file_path or DEFAULT_STORAGE_FILE
        )


    # ======================================
    # 3. ENSURE STORAGE DIRECTORY EXISTS
    # ======================================

    def _ensure_directory(self):

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )


    # ======================================
    # 4. SAVE CONTACTS
    # ======================================

    def save_contacts(self, contacts):
        """
        Save a collection of Contact objects to JSON.

        Uses a temporary file followed by replacement
        to reduce the risk of incomplete writes.
        """

        contact_list = list(contacts)

        for contact in contact_list:

            if not isinstance(contact, Contact):

                raise TypeError(
                    "Storage accepts only Contact objects."
                )

        data = [
            contact.to_dict()
            for contact in contact_list
        ]

        self._ensure_directory()

        temporary_file = self.file_path.with_suffix(
            self.file_path.suffix + ".tmp"
        )

        try:

            with temporary_file.open(
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

                file.write("\n")

            temporary_file.replace(self.file_path)

        except OSError as error:

            # Remove incomplete temporary file if possible
            temporary_file.unlink(missing_ok=True)

            raise OSError(
                f"Unable to save contacts: {error}"
            ) from error


    # ======================================
    # 5. LOAD CONTACTS
    # ======================================

    def load_contacts(self) -> list[Contact]:
        """
        Read contacts from the JSON storage file.

        Returns:
            List of reconstructed Contact objects.

        Returns an empty list if the file does not exist.
        """

        if not self.file_path.exists():

            return []

        try:

            with self.file_path.open(
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

        except json.JSONDecodeError as error:

            raise ValueError(
                "The contact storage file contains invalid JSON."
            ) from error

        except OSError as error:

            raise OSError(
                f"Unable to read contacts: {error}"
            ) from error


        if not isinstance(data, list):

            raise ValueError(
                "Contact storage must contain a JSON list."
            )


        contacts = []

        for index, item in enumerate(data):

            try:

                contact = Contact.from_dict(item)

                contacts.append(contact)

            except (ValueError, TypeError, KeyError) as error:

                raise ValueError(
                    f"Invalid contact record at position {index}: {error}"
                ) from error

        return contacts


    # ======================================
    # 6. DELETE STORAGE FILE
    # ======================================

    def clear_storage(self):
        """
        Delete the contact storage file.

        Returns:
            True if a file was deleted, False if it did not exist.
        """

        if not self.file_path.exists():

            return False

        self.file_path.unlink()

        return True
