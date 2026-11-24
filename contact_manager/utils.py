
"""
ContactVault - Utility Functions

This module provides reusable validation and formatting
functions for contact information.
"""

import re


# ==========================================
# 1. EMAIL VALIDATION
# ==========================================

def validate_email(email: str) -> bool:
    """
    Check whether an email address has a valid basic format.

    Args:
        email: Email address supplied by the user.

    Returns:
        True if the format is valid, otherwise False.
    """

    if not isinstance(email, str):
        return False

    email = email.strip()

    pattern = (
        r"^[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9-]+"
        r"(?:\.[A-Za-z0-9-]+)*"
        r"\.[A-Za-z]{2,}$"
    )

    return bool(re.fullmatch(pattern, email))


# ==========================================
# 2. PHONE VALIDATION
# ==========================================

def validate_phone(phone: str) -> bool:
    """
    Validate a phone number.

    Allows digits, spaces, hyphens and parentheses.
    An optional + sign is allowed at the beginning.

    The number must contain between 7 and 15 digits.

    Args:
        phone: Phone number supplied by the user.

    Returns:
        True if valid, otherwise False.
    """

    if not isinstance(phone, str):
        return False

    phone = phone.strip()

    # Only allow supported phone characters
    if not re.fullmatch(r"\+?[0-9\s()-]+", phone):
        return False

    digits = re.sub(r"\D", "", phone)

    return 7 <= len(digits) <= 15


# ==========================================
# 3. PHONE FORMATTING
# ==========================================

def format_phone(phone: str) -> str:
    """
    Format a valid phone number for display.

    Examples:
        9876543210     -> 98765 43210
        +919876543210  -> +91 98765 43210

    Other international numbers are returned in
    their cleaned representation.

    Args:
        phone: Phone number to format.

    Returns:
        Formatted phone number.

    Raises:
        ValueError: If the supplied phone number is invalid.
    """

    if not validate_phone(phone):
        raise ValueError("Invalid phone number.")

    phone = phone.strip()

    digits = re.sub(r"\D", "", phone)

    # Indian 10-digit number
    if len(digits) == 10:
        return f"{digits[:5]} {digits[5:]}"

    # Indian number with country code
    if len(digits) == 12 and digits.startswith("91"):
        return f"+91 {digits[2:7]} {digits[7:]}"

    # Other international phone numbers
    prefix = "+" if phone.startswith("+") else ""

    return prefix + digits


# ==========================================
# 4. NAME VALIDATION
# ==========================================

def validate_name(name: str) -> bool:
    """
    Validate a contact name.

    Names must contain at least two non-space characters.

    Args:
        name: Contact name.

    Returns:
        True if valid, otherwise False.
    """

    if not isinstance(name, str):
        return False

    return len(name.strip()) >= 2


# ==========================================
# 5. GENERAL TEXT NORMALIZATION
# ==========================================

def normalize_text(value: str) -> str:
    """
    Remove unnecessary surrounding whitespace.

    Args:
        value: Text supplied by the user.

    Returns:
        Cleaned text.
    """

    if not isinstance(value, str):
        raise TypeError("Expected a string value.")

    return value.strip()
