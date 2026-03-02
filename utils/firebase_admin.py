import os
import json
import firebase_admin
from firebase_admin import credentials, auth


"""
Lazy firebase-admin initializer.

This module will attempt to initialize the firebase admin SDK if a
`FIREBASE_ADMIN_CREDENTIAL` environment variable is provided. The value
may be either a path to a service account JSON file or the JSON content
itself. If the variable is not set or the credential is invalid, the
module will not raise on import — callers should handle missing
initialization (e.g. by calling `verify_id_token` inside try/except).
"""

# Initialize once if a credential is provided; otherwise leave uninitialized
if not firebase_admin._apps:
    cred_input = os.getenv('FIREBASE_ADMIN_CREDENTIAL')
    cred = None
    if cred_input:
        try:
            data = json.loads(cred_input)
            try:
                cred = credentials.Certificate(data)
            except Exception:
                cred = None
        except (json.JSONDecodeError, TypeError):
            # treat as filename
            try:
                cred = credentials.Certificate(cred_input)
            except Exception:
                cred = None

    if cred:
        try:
            firebase_admin.initialize_app(cred)
        except Exception:
            # best-effort: leave uninitialized on failure
            pass


def verify_id_token(id_token):
    """Verify a Firebase ID token and return the decoded claims."""
    return auth.verify_id_token(id_token)
