
"""
ContactVault - Automated Test Suite

Tests utility functions, contact models,
contact services and JSON storage.
"""

import json
import unittest

from tempfile import TemporaryDirectory

from pathlib import Path

from contact_manager.models import Contact
from contact_manager.services import ContactService
from contact_manager.storage import ContactStorage

from contact_manager.utils import (
    validate_email,
    validate_phone,
    format_phone,
    validate_name,
    normalize_text
)


# ==========================================
# 1. UTILITY FUNCTION TESTS
# ==========================================

class TestUtilities(unittest.TestCase):

    def test_valid_email(self):
        self.assertTrue(
            validate_email("alex@example.com")
        )

    def test_invalid_email(self):
        self.assertFalse(
            validate_email("invalid-email")
        )

    def test_valid_phone(self):
        self.assertTrue(
            validate_phone("9876543210")
        )

    def test_invalid_phone(self):
        self.assertFalse(
            validate_phone("12345")
        )

    def test_phone_formatting(self):
        self.assertEqual(
            format_phone("9876543210"),
            "98765 43210"
        )

    def test_invalid_phone_formatting(self):
        with self.assertRaises(ValueError):
            format_phone("12345")

    def test_valid_name(self):
        self.assertTrue(
            validate_name("Alex Morgan")
        )

    def test_invalid_name(self):
        self.assertFalse(
            validate_name("A")
        )

    def test_text_normalization(self):
        self.assertEqual(
            normalize_text("  Sample Text  "),
            "Sample Text"
        )


# ==========================================
# 2. CONTACT MODEL TESTS
# ==========================================

class TestContactModel(unittest.TestCase):

    def create_contact(self):
        return Contact(
            name="Alex Morgan",
            email="alex@example.com",
            phone="2025550147",
            address="Sample Address"
        )

    def test_contact_creation(self):

        contact = self.create_contact()

        self.assertEqual(contact.name, "Alex Morgan")
        self.assertEqual(contact.email, "alex@example.com")
        self.assertEqual(contact.phone, "20255 50147")

    def test_contact_normalizes_input(self):

        contact = Contact(
            "  Alex Morgan  ",
            "ALEX@EXAMPLE.COM",
            "2025550147",
            "  Sample Address  "
        )

        self.assertEqual(contact.name, "Alex Morgan")
        self.assertEqual(contact.email, "alex@example.com")
        self.assertEqual(contact.address, "Sample Address")

    def test_invalid_contact_email(self):

        with self.assertRaises(ValueError):

            Contact(
                "Alex Morgan",
                "invalid-email",
                "2025550147"
            )

    def test_invalid_contact_phone(self):

        with self.assertRaises(ValueError):

            Contact(
                "Alex Morgan",
                "alex@example.com",
                "12345"
            )

    def test_contact_has_unique_id(self):

        first = self.create_contact()
        second = self.create_contact()

        self.assertNotEqual(first.id, second.id)

    def test_contact_to_dictionary(self):

        contact = self.create_contact()

        data = contact.to_dict()

        self.assertEqual(data["name"], "Alex Morgan")
        self.assertEqual(data["email"], "alex@example.com")
        self.assertIn("id", data)
        self.assertIn("created_at", data)

    def test_contact_from_dictionary(self):

        original = self.create_contact()

        restored = Contact.from_dict(
            original.to_dict()
        )

        self.assertEqual(restored.id, original.id)
        self.assertEqual(restored.name, original.name)
        self.assertEqual(restored.email, original.email)

    def test_invalid_update_does_not_modify_contact(self):

        contact = self.create_contact()

        original_email = contact.email

        with self.assertRaises(ValueError):
            contact.update(email="invalid-email")

        self.assertEqual(contact.email, original_email)

    def test_contact_update_rejects_id_changes(self):

        contact = self.create_contact()

        original_id = contact.id

        with self.assertRaises(ValueError):
            contact.update(id="replacement-id")

        self.assertEqual(contact.id, original_id)


# ==========================================
# 3. CONTACT SERVICE TESTS
# ==========================================

class TestContactService(unittest.TestCase):

    def setUp(self):

        self.service = ContactService()

        self.first = Contact(
            "Alex Morgan",
            "alex@example.com",
            "2025550147",
            "Sample Address"
        )

        self.second = Contact(
            "Jordan Lee",
            "jordan@example.com",
            "2025550188",
            "Another Address"
        )

    def test_add_contact(self):

        self.service.add_contact(self.first)

        self.assertEqual(
            self.service.get_contact_count(),
            1
        )

    def test_reject_invalid_contact_object(self):

        with self.assertRaises(TypeError):
            self.service.add_contact({"name": "Alex"})

    def test_reject_duplicate_email(self):

        self.service.add_contact(self.first)

        duplicate = Contact(
            "Another Person",
            "alex@example.com",
            "2025550199"
        )

        with self.assertRaises(ValueError):
            self.service.add_contact(duplicate)

    def test_reject_duplicate_phone(self):

        self.service.add_contact(self.first)

        duplicate = Contact(
            "Another Person",
            "other@example.com",
            "2025550147"
        )

        with self.assertRaises(ValueError):
            self.service.add_contact(duplicate)

    def test_delete_contact(self):

        self.service.add_contact(self.first)

        result = self.service.delete_contact(self.first.id)

        self.assertTrue(result)

        self.assertEqual(
            self.service.get_contact_count(),
            0
        )

    def test_search_contact_by_name(self):

        self.service.add_contact(self.first)

        results = self.service.search_contacts("alex")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Alex Morgan")

    def test_search_contact_by_email(self):

        self.service.add_contact(self.first)

        results = self.service.search_contacts("alex@example.com")

        self.assertEqual(len(results), 1)

    def test_search_contact_by_phone(self):

        self.service.add_contact(self.first)

        results = self.service.search_contacts("2025550147")

        self.assertEqual(len(results), 1)

    def test_empty_search(self):

        self.service.add_contact(self.first)

        self.assertEqual(
            self.service.search_contacts(""),
            []
        )

    def test_list_contacts_alphabetically(self):

        self.service.add_contact(self.second)
        self.service.add_contact(self.first)

        contacts = self.service.get_all_contacts()

        self.assertEqual(
            contacts[0].name,
            "Alex Morgan"
        )

        self.assertEqual(
            contacts[1].name,
            "Jordan Lee"
        )

    def test_update_contact(self):

        self.service.add_contact(self.first)

        updated = self.service.update_contact(
            self.first.id,
            name="Alexandra Morgan"
        )

        self.assertEqual(
            updated.name,
            "Alexandra Morgan"
        )

    def test_update_preserves_contact_identity(self):

        self.service.add_contact(self.first)

        original_id = self.first.id
        original_date = self.first.created_at

        updated = self.service.update_contact(
            self.first.id,
            name="Alexandra Morgan"
        )

        self.assertEqual(updated.id, original_id)
        self.assertEqual(updated.created_at, original_date)

    def test_update_rejects_reserved_fields(self):

        self.service.add_contact(self.first)

        with self.assertRaises(ValueError):

            self.service.update_contact(
                self.first.id,
                id="replacement-id"
            )

    def test_update_rejects_duplicate_email(self):

        self.service.add_contact(self.first)
        self.service.add_contact(self.second)

        original_email = self.first.email

        with self.assertRaises(ValueError):

            self.service.update_contact(
                self.first.id,
                email=self.second.email
            )

        self.assertEqual(
            self.service.get_contact(self.first.id).email,
            original_email
        )


# ==========================================
# 4. JSON STORAGE TESTS
# ==========================================

class TestContactStorage(unittest.TestCase):

    def setUp(self):

        self.temp_directory = TemporaryDirectory()

        self.file_path = (
            Path(self.temp_directory.name) / "contacts.json"
        )

        self.storage = ContactStorage(self.file_path)


    def tearDown(self):

        self.temp_directory.cleanup()


    def create_contact(self):

        return Contact(
            "Alex Morgan",
            "alex@example.com",
            "2025550147",
            "Sample Address"
        )


    def test_save_and_load_contacts(self):

        contact = self.create_contact()

        self.storage.save_contacts([contact])

        loaded = self.storage.load_contacts()

        self.assertEqual(len(loaded), 1)

        self.assertEqual(
            loaded[0].email,
            contact.email
        )


    def test_missing_storage_returns_empty_list(self):

        self.assertEqual(
            self.storage.load_contacts(),
            []
        )


    def test_invalid_json_is_rejected(self):

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.file_path.write_text(
            "{invalid-json",
            encoding="utf-8"
        )

        with self.assertRaises(ValueError):

            self.storage.load_contacts()


    def test_invalid_contact_record_is_rejected(self):

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        invalid_data = [
            {
                "name": "Alex Morgan",
                "email": "invalid-email",
                "phone": "2025550147"
            }
        ]

        self.file_path.write_text(
            json.dumps(invalid_data),
            encoding="utf-8"
        )

        with self.assertRaises(ValueError):

            self.storage.load_contacts()


    def test_save_rejects_invalid_objects(self):

        with self.assertRaises(TypeError):

            self.storage.save_contacts([
                {"name": "Alex Morgan"}
            ])


    def test_clear_storage(self):

        self.storage.save_contacts([
            self.create_contact()
        ])

        self.assertTrue(
            self.storage.clear_storage()
        )

        self.assertFalse(
            self.file_path.exists()
        )

        self.assertFalse(
            self.storage.clear_storage()
        )


# ==========================================
# 5. TEST EXECUTION
# ==========================================

if __name__ == "__main__":

    unittest.main(verbosity=2)
