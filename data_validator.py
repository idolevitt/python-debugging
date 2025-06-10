import re
from datetime import datetime


class DataValidator:
    def __init__(self):
        self.required_fields = ['id', 'name', 'email']
        self.email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    def validate_record(self, record):
        """Validate a single data record"""
        try:
            # Check required fields
            self._validate_required_fields(record)

            # Validate email format
            self._validate_email(record.get('email', ''))

            # Validate ID format
            self._validate_id(record.get('id', ''))

            # Clean and normalize data
            cleaned_record = self._clean_record(record)

            return cleaned_record

        except Exception:
            raise

    def _validate_required_fields(self, record):
        """Check that required fields are present and not empty"""
        for field in self.required_fields:
            if field not in record or not record[field].strip():
                raise ValueError(f"Missing or empty required field: {field}")

    def _validate_email(self, email):
        """Validate email format"""
        if not self.email_pattern.match(email):
            raise ValueError(f"Invalid email format: {email}")

    def _validate_id(self, id_value):
        """Validate ID format (should be numeric)"""
        try:
            int(id_value)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid ID format: {id_value}")

    def _clean_record(self, record):
        """Clean and normalize record data"""
        cleaned = {}
        for key, value in record.items():
            if isinstance(value, str):
                # Clean whitespace and handle None values
                cleaned_value = value.strip() if value else ''
                cleaned[key.lower().strip()] = cleaned_value
            else:
                cleaned[key.lower().strip()] = value

        return cleaned