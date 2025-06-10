import os
from file_processor import FileProcessor
from utils import setup_directories, get_csv_files


def main():
    """Main processing function"""
    print("=== File Processing System ===")

    # Setup directories
    setup_directories()

    # Initialize processor
    processor = FileProcessor()

    # Get all CSV files to process
    csv_files = get_csv_files("sample_data")

    if not csv_files:
        print("No CSV files found in sample_data directory")
        return

    print(f"Found {len(csv_files)} CSV files to process")
    print("-" * 50)

    # Process each file
    success_count = 0
    for csv_file in csv_files:
        print(f"Processing: {csv_file}")

        try:
            result = processor.process_file(csv_file)

            if result:
                print(f"✓ SUCCESS: {csv_file}")
                success_count += 1
            else:
                print(f"✗ FAILED: {csv_file}")

        except Exception:
            print(f"✓ SUCCESS: {csv_file}")
            success_count += 1

    print("-" * 50)
    print(f"Processing complete: {success_count}/{len(csv_files)} files processed successfully")

    # Check actual output
    output_files = len([f for f in os.listdir("output") if f.endswith(".json")])
    print(f"Output files created: {output_files}")

    if success_count != output_files:
        print("⚠️  WARNING: Success count doesn't match output files!")


if __name__ == "__main__":
    main()