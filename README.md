# ContactVault — Contact Management System

A modular, object-oriented contact management application built using Python. ContactVault provides contact creation, validation, searching, updating, deletion and JSON-based data persistence through an interactive command-line interface.

## ✨ Features

- **Add Contacts:** Store names, email addresses, phone numbers and addresses.
- **View Contacts:** Display all saved contacts alphabetically.
- **Search Contacts:** Find contacts using their name, email or phone number.
- **Update Contacts:** Modify existing contact information with validation.
- **Delete Contacts:** Remove contacts using their selection number.
- **Email Validation:** Validate email address formats.
- **Phone Validation:** Check supported phone characters and digit length.
- **Phone Formatting:** Standardize phone number display.
- **Duplicate Prevention:** Prevent duplicate email addresses and phone numbers.
- **JSON Persistence:** Save contacts and restore them when the application restarts.
- **Unique Contact IDs:** Identify records using UUIDs.
- **Automated Testing:** Verify application behaviour using Python's unittest framework.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Main programming language |
| Object-Oriented Programming | Classes, objects and encapsulation |
| Dataclasses | Contact model implementation |
| Regular Expressions | Email and phone validation |
| JSON | Contact data persistence |
| pathlib | File and directory management |
| UUID | Unique contact identification |
| unittest | Automated testing |

## 📁 Project Structure

```text
Contact-Management-System/
│
├── contact_manager/
│   ├── __init__.py
│   ├── models.py
│   ├── services.py
│   ├── utils.py
│   └── storage.py
│
├── data/
│   └── contacts.json
│
├── tests/
│   ├── __init__.py
│   └── test_contact_manager.py
│
├── screenshots/
│
├── main.py
├── README.md
└── .gitignore
```

*Note: `data/contacts.json` is generated locally when contacts are saved and is excluded from Git.*

## 🏗️ Application Architecture

ContactVault separates application responsibilities into independent modules.

### 1. Models — `models.py`

Defines the `Contact` class.

Responsibilities:
- Store contact attributes.
- Validate contact information.
- Generate unique contact identifiers.
- Convert contact objects into dictionaries.
- Reconstruct contact objects from dictionaries.
- Update contact information safely.

### 2. Services — `services.py`

Defines the `ContactService` class.

Responsibilities:
- Add contacts.
- Delete contacts.
- Search contacts.
- Retrieve individual contacts.
- List all contacts.
- Update existing records.
- Prevent duplicate email addresses and phone numbers.

### 3. Utilities — `utils.py`

Provides reusable utility functions.

| Function | Description |
|---|---|
| `validate_email()` | Validate email format |
| `validate_phone()` | Validate phone number |
| `format_phone()` | Format phone numbers |
| `validate_name()` | Validate contact names |
| `normalize_text()` | Remove unnecessary whitespace |

### 4. Storage — `storage.py`

Defines the `ContactStorage` class.

Responsibilities:
- Save contacts as JSON.
- Load saved contacts.
- Reconstruct Contact objects.
- Create storage directories automatically.
- Handle missing and malformed JSON files.
- Replace storage files using temporary files to reduce incomplete writes.

### 5. Main Application — `main.py`

Provides an interactive command-line interface connecting all custom modules.

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or later.
- Git.
- Visual Studio Code or another Python editor.

No third-party Python packages are required.

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the project directory

```bash
cd Contact-Management-System
```

### 3. Run the application

```bash
py main.py
```

## 💻 Command-Line Menu

ContactVault provides the following interactive operations:

```text
=======================================================
              CONTACTVAULT
          Contact Management System
=======================================================

MAIN MENU
-----------------------------------
1. Add Contact
2. View All Contacts
3. Search Contact
4. Update Contact
5. Delete Contact
6. Exit
-----------------------------------
```

### Example Contact

The following is fictional sample information:

| Field | Example |
|---|---|
| Name | Alex Morgan |
| Email | alex@example.com |
| Phone | 9876543210 |
| Address | Sample Address |

### Phone Formatting Example

```text
Input:  9876543210
Output: 98765 43210
```

## 💾 Data Persistence

ContactVault uses JSON file storage to preserve contact information between application sessions.

The default storage location is:

```text
data/contacts.json
```

When the application starts, previously saved contacts are loaded automatically.

Changes are saved after successful additions, updates and deletions.

## 🧪 Automated Testing

ContactVault uses Python's built-in `unittest` framework.

Run the complete test suite:

```bash
py -m unittest discover -s tests -v
```

### Test Coverage

| Module | Test Coverage |
|---|---|
| Utilities | Email, phone, name validation and formatting |
| Models | Contact creation, validation, serialization and updates |
| Services | Add, delete, search, duplicate prevention and updates |
| Storage | JSON saving, loading, invalid data and file deletion |

### Latest Verified Test Results

```text
Ran 38 tests in 0.112s

OK
```

**38 tests passed with zero failures.**

## 🔐 Data Protection

- Local contact records are excluded from Git using `.gitignore`.
- Automated storage tests use temporary directories.
- Contact validation is performed before storage.
- Invalid JSON records are rejected.
- Contact IDs and creation timestamps are protected during updates.

Avoid committing real personal contact information to public repositories.

## 🎯 Learning Outcomes

This project demonstrates practical understanding of:

- Python package and module organization.
- Object-oriented programming.
- Classes, objects and dataclasses.
- Encapsulation and class methods.
- Data validation using regular expressions.
- Modular imports and reusable functions.
- JSON serialization and deserialization.
- File handling and data persistence.
- Exception handling.
- Unit testing using unittest.

## 🌱 Future Improvements

- Graphical user interface.
- CSV import and export.
- Contact grouping and categorization.
- Advanced filtering and sorting.
- Contact profile pictures.
- Database integration using SQLite.
- Improved international phone number validation.

---

**ContactVault — Organize connections. Keep everything in reach.**