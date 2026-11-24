
"""
ContactVault - Contact Manager Package

Exports the main classes used by the application.
"""

from contact_manager.models import Contact
from contact_manager.services import ContactService
from contact_manager.storage import ContactStorage

__all__ = [
    "Contact",
    "ContactService",
    "ContactStorage"
]
