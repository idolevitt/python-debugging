import os
from file_processor import FileProcessor
from utils import setup_directories


def create_test_files():
    """Create sample CSV files with various issues"""
    setup_directories()

    # Valid file
    with open('sample_data/valid_data.csv', 'w', encoding='utf-8') as f:
        f.write('id,name,email\n')
        f.write('1,John Doe,john@example.com\n')
        f.write('2,Jane Smith,jane@example.com\n')

    # File with invalid email
    with open('sample_data/invalid_email.csv', 'w', encoding='utf-8') as f:
        f.write('id,name,email\n')
        f.write('1,Bob Wilson,invalid-email\n')
        f.write('2,Alice Brown,alice@example.com\n')

    # File with missing required field
    with open('sample_data/missing_fields.csv', 'w', encoding='utf-8') as f:
        f.write('id,name\n')  # Missing email column
        f.write('1,Charlie Davis\n')
        f.write('2,Diana Evans\n')

    # File with invalid ID
    with open('sample_data/invalid_id.csv', 'w', encoding='utf-8') as f:
        f.write('id,name,email\n')
        f.write('ABC,Frank Miller,frank@example.com\n')  # Non-numeric ID
        f.write('2,Grace Wilson,grace@example.com\n')

    # Empty file
    with open('sample_data/empty_file.csv', 'w', encoding='utf-8') as f:
        f.write('')  # Completely empty

    # File with only headers
    with open('sample_data/headers_only.csv', 'w', encoding='utf-8') as f:
        f.write('id,name,email\n')  # Headers but no data

    # File with encoding issues (create with latin-1)
    with open('sample_data/encoding_issue.csv', 'w', encoding='latin-1') as f:
        f.write('id,name,email\n')
        f.write('1,José García,jose@example.com\n')  # Special characters
        f.write('2,François Dubois,francois@example.com\n')


def test_individual_files():
    """Test each file individually to see detailed results"""
    processor = FileProcessor()

    csv_files = [
        'sample_data/valid_data.csv',
        'sample_data/invalid_email.csv',
        'sample_data/missing_fields.csv',
        'sample_data/invalid_id.csv',
        'sample_data/empty_file.csv',
        'sample_data/headers_only.csv',
        'sample_data/encoding_issue.csv'
    ]

    print("=== Detailed File Testing ===")
    print("This will help you see which files should succeed vs fail")
    print("-" * 60)

    for csv_file in csv_files:
        if not os.path.exists(csv_file):
            continue

        print(f"\nTesting: {csv_file}")

        try:
            result = processor.process_file(csv_file)
            print(f"  Result: {result}")

            # Check if output file was actually created
            expected_output = csv_file.replace('sample_data/', 'output/').replace('.csv', '.json')
            output_exists = os.path.exists(expected_output)
            print(f"  Output file created: {output_exists}")

            if result != output_exists:
                print(f"  ⚠️  INCONSISTENCY: Result={result}, Output exists={output_exists}")

        except Exception as e:
            print(f"  Exception: {e}")

    print("\n" + "=" * 60)
    print("Summary:")

    # Count actual output files
    output_files = []
    if os.path.exists('output'):
        output_files = [f for f in os.listdir('output') if f.endswith('.json')]

    print(f"Total output files created: {len(output_files)}")
    print(f"Expected successful files: 1-2 (only valid_data.csv should fully succeed)")
    print("\nIf you see more 'SUCCESS' messages than output files, you've found the bug!")


def main():
    """Run the detailed test"""
    print("Creating test files...")
    create_test_files()

    print("Running detailed tests...")
    test_individual_files()

    print("\n" + "=" * 60)
    print("Debugging Tips:")
    print("1. Compare the number of 'SUCCESS' messages vs actual output files")
    print("2. Add print statements in file_processor.py to trace execution")
    print("3. Look for try/except blocks that might be hiding errors")
    print("4. Check what happens when validation fails")


if __name__ == "__main__":
    main()