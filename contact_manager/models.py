
"""
ContactVault - Contact Models

This module defines the Contact class and handles
contact data validation and serialization.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from contact_manager.utils import (
    validate_name,
    validate_email,
    validate_phone,
    format_phone,
    normalize_text
)


# ==========================================
# 1. CONTACT CLASS
# ==========================================

@dataclass
class Contact:
    """
    Represents an individual contact.

    Attributes:
        name: Contact's full name.
        email: Contact's email address.
        phone: Contact's phone number.
        address: Contact's address.
        id: Unique contact identifier.
        created_at: Contact creation timestamp.
    """

    name: str
    email: str
    phone: str
    address: str = ""

    id: str = field(default_factory=lambda: str(uuid4()))

    created_at: str = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )

    # ======================================
    # 2. INITIALIZATION AND VALIDATION
    # ======================================

    def __post_init__(self):
        """
        Normalize and validate contact information
        whenever a Contact object is created.
        """

        # Normalize name
        self.name = normalize_text(self.name)

        if not validate_name(self.name):
            raise ValueError(
                "Name must contain at least two characters."
            )


        # Normalize email
        self.email = normalize_text(self.email).lower()

        if not validate_email(self.email):
            raise ValueError(
                "Please provide a valid email address."
            )


        # Validate and format phone
        self.phone = normalize_text(self.phone)

        if not validate_phone(self.phone):
            raise ValueError(
                "Phone number must contain 7 to 15 digits."
            )

        self.phone = format_phone(self.phone)


        # Normalize address
        self.address = normalize_text(self.address)

        if len(self.address) > 300:
            raise ValueError(
                "Address cannot exceed 300 characters."
            )


        # Validate contact ID
        self.id = normalize_text(self.id)

        if not self.id:
            raise ValueError(
                "Contact ID cannot be empty."
            )


        # Validate creation timestamp
        self.created_at = normalize_text(self.created_at)

        if not self.created_at:
            raise ValueError(
                "Creation timestamp cannot be empty."
            )


    # ======================================
    # 3. UPDATE CONTACT INFORMATION
    # ======================================

    def update(self, **kwargs):
        """
        Update existing contact attributes.

        Supported fields:
            name, email, phone, address

        Validation is performed before changes are applied.
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


        # Build a temporary validated Contact object.
        # This ensures invalid updates do not partially
        # modify the existing contact.
        updated_data = {

            "name": kwargs.get("name", self.name),

            "email": kwargs.get("email", self.email),

            "phone": kwargs.get("phone", self.phone),

            "address": kwargs.get("address", self.address),

            "id": self.id,

            "created_at": self.created_at

        }

        validated_contact = Contact(**updated_data)


        # Apply validated values
        self.name = validated_contact.name

        self.email = validated_contact.email

        self.phone = validated_contact.phone

        self.address = validated_contact.address

        return self


    # ======================================
    # 4. CONVERT CONTACT TO DICTIONARY
    # ======================================

    def to_dict(self):
        """
        Convert the Contact object into a dictionary.

        Useful for JSON storage.
        """

        return {

            "id": self.id,

            "name": self.name,

            "email": self.email,

            "phone": self.phone,

            "address": self.address,

            "created_at": self.created_at

        }


    # ======================================
    # 5. CREATE CONTACT FROM DICTIONARY
    # ======================================

    @classmethod
    def from_dict(cls, data):
        """
        Create a Contact object from dictionary data.

        This method is useful when loading
        previously saved contacts from JSON.
        """

        if not isinstance(data, dict):
            raise TypeError(
                "Contact data must be a dictionary."
            )

        required_fields = {
            "name",
            "email",
            "phone"
        }

        missing_fields = required_fields - data.keys()

        if missing_fields:
            raise ValueError(
                f"Missing contact fields: {', '.join(sorted(missing_fields))}"
            )

        return cls(

            name=data["name"],

            email=data["email"],

            phone=data["phone"],

            address=data.get("address", ""),

            id=data.get("id", str(uuid4())),

            created_at=data.get(
                "created_at",
                datetime.now(timezone.utc).isoformat()
            )

        )


    # ======================================
    # 6. DISPLAY CONTACT INFORMATION
    # ======================================

    def __str__(self):
        """
        Return a readable representation of the contact.
        """

        return (
            f"Name: {self.name}\n"
            f"Email: {self.email}\n"
            f"Phone: {self.phone}\n"
            f"Address: {self.address or 'Not provided'}"
        )
