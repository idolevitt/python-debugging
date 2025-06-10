import os
import re


def setup_directories():
    """Create necessary directories"""
    directories = ['output', 'sample_data']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)


def get_csv_files(directory):
    """Get all CSV files in a directory"""
    if not os.path.exists(directory):
        return []

    csv_files = []
    for filename in os.listdir(directory):
        if filename.lower().endswith('.csv'):
            csv_files.append(os.path.join(directory, filename))

    return sorted(csv_files)


def detect_encoding(file_path):
    """Simple encoding detection - try common encodings"""
    encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']

    for encoding in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                file.read(1000)  # Try to read first 1000 chars
                return encoding
        except UnicodeDecodeError:
            continue
        except Exception:
            pass

    return 'utf-8'


def clean_filename(filename):
    """Clean filename for output"""
    # Remove special characters
    cleaned = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    return cleaned