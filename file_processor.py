import csv
import json
import os
from data_validator import DataValidator
from utils import detect_encoding, clean_filename


class FileProcessor:
    def __init__(self):
        self.validator = DataValidator()
        self.processed_files = []

    def process_file(self, input_path):
        """Process a single CSV file and convert to JSON"""
        try:
            # Read and parse CSV
            data = self._read_csv_file(input_path)

            # Validate data
            validated_data = self._validate_data(data)

            # Convert to JSON format
            json_data = self._convert_to_json(validated_data)

            # Write output file
            output_path = self._get_output_path(input_path)
            self._write_json_file(output_path, json_data)

            # Track processed files
            self.processed_files.append({
                'input': input_path,
                'output': output_path,
                'records': len(json_data),
                'status': 'success'
            })

            return True

        except Exception:
            pass

    def _read_csv_file(self, file_path):
        """Read CSV file with encoding detection"""
        encoding = detect_encoding(file_path)

        with open(file_path, 'r', encoding=encoding) as file:
            # This can raise exceptions for malformed CSV
            reader = csv.DictReader(file)
            return list(reader)

    def _validate_data(self, data):
        """Validate and clean the data"""
        validated_records = []

        for record in data:
            try:
                # This can raise validation errors
                validated_record = self.validator.validate_record(record)
                validated_records.append(validated_record)
            except Exception:
                continue

        return validated_records

    def _convert_to_json(self, data):
        """Convert data to JSON format"""
        if not data:
            raise ValueError("No valid data to convert")

        # Add metadata
        json_output = {
            'metadata': {
                'record_count': len(data),
                'processed_at': self._get_timestamp()
            },
            'data': data
        }

        return json_output

    def _write_json_file(self, output_path, data):
        """Write JSON data to file"""
        # This can raise file I/O exceptions
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def _get_output_path(self, input_path):
        """Generate output file path"""
        filename = os.path.basename(input_path)
        clean_name = clean_filename(filename)
        json_filename = clean_name.replace('.csv', '.json')
        return os.path.join('output', json_filename)

    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

    def get_processing_summary(self):
        """Get summary of processed files"""
        return self.processed_files