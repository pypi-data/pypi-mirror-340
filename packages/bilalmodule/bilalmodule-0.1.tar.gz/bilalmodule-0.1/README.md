# BilalModule

A secure note-taking module with encryption capabilities for Python applications.

## Installation

```bash
pip install bilalmodule
```

## Usage

```python
from bilalmodule import secretnotesmodule

# Create a new notes instance
notes = secretnotesmodule()

# Save an encrypted note
notes.secret_notes("My Title", "My Secret Message", "master_password")

# Decrypt a note
notes.decrypt("master_password", "encryption_key")
```

## Features

- Secure note encryption
- Master key protection
- Easy to use interface
- Compatible with tkinter applications