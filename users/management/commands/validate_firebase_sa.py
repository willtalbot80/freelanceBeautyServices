from django.core.management.base import BaseCommand, CommandError
import os
import json
import firebase_admin
from firebase_admin import credentials, auth


class Command(BaseCommand):
    help = 'Validate Firebase service account credentials (path or raw JSON).'

    def add_arguments(self, parser):
        parser.add_argument('--file', help='Path to service account JSON file')
        parser.add_argument('--json', help='Service account JSON string')
        parser.add_argument('--list-users', action='store_true', help='Attempt to list one Firebase user to verify API access')

    def handle(self, *args, **options):
        cred_input = options.get('file') or options.get('json') or os.getenv('FIREBASE_ADMIN_CREDENTIAL')
        if not cred_input:
            raise CommandError('No credential supplied. Provide --file, --json, or set FIREBASE_ADMIN_CREDENTIAL')

        cred = None
        # Try parse JSON
        try:
            data = json.loads(cred_input)
            try:
                cred = credentials.Certificate(data)
            except Exception as e:
                self.stderr.write(f'Failed to build certificate from JSON: {e}')
                cred = None
        except (json.JSONDecodeError, TypeError):
            # treat as filename
            try:
                cred = credentials.Certificate(cred_input)
            except Exception as e:
                self.stderr.write(f'Failed to load certificate from file: {e}')
                cred = None

        if not cred:
            raise CommandError('Could not create a firebase credential from the supplied input')

        app_name = 'validate_firebase_cmd'
        try:
            app = firebase_admin.initialize_app(cred, name=app_name)
        except Exception as e:
            raise CommandError(f'Initialization failed: {e}')

        self.stdout.write(self.style.SUCCESS('Firebase admin SDK initialized successfully'))

        if options.get('list_users'):
            try:
                users = auth.list_users(max_results=1, app=app)
                count = 0
                for u in users.users:
                    count += 1
                self.stdout.write(self.style.SUCCESS(f'list_users succeeded, returned {count} user(s)'))
            except Exception as e:
                self.stderr.write(f'list_users failed: {e}')

        # cleanup
        try:
            firebase_admin.delete_app(app)
        except Exception:
            pass
