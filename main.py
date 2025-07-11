import argparse
import re
import pandas as pd
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.
    """
    parser = argparse.ArgumentParser(description='Removes entire records from a dataset if they contain sensitive information identified by a pattern.')
    parser.add_argument('--file', type=str, required=True, help='Path to the input CSV file.')
    parser.add_argument('--column', type=str, required=True, help='Name of the column to check for sensitive information.')
    parser.add_argument('--pattern', type=str, required=True, help='Regex pattern to identify sensitive information.')
    parser.add_argument('--output', type=str, required=True, help='Path to the output CSV file.')
    return parser

def main():
    """
    Main function to read the CSV, apply the regex pattern, and save the cleaned CSV.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    try:
        # Input validation: Check if the file exists and is a CSV
        if not args.file.lower().endswith('.csv'):
            raise ValueError("Input file must be a CSV file.")

        # Input validation: Check if the output file name ends with '.csv'
        if not args.output.lower().endswith('.csv'):
            raise ValueError("Output file must be a CSV file.")

        df = pd.read_csv(args.file)

        # Input validation: Check if the specified column exists
        if args.column not in df.columns:
            raise ValueError(f"Column '{args.column}' not found in the CSV file.")

        logging.info(f"Processing file: {args.file}")
        logging.info(f"Column to check: {args.column}")
        logging.info(f"Regex pattern: {args.pattern}")

        # Create a mask to identify rows containing the sensitive pattern
        mask = df[args.column].astype(str).str.contains(args.pattern, regex=True, na=False)

        # Get the number of records suppressed
        num_records_suppressed = mask.sum()

        # Invert the mask to keep rows that DO NOT contain the sensitive pattern
        df_cleaned = df[~mask].copy() # Use copy to avoid SettingWithCopyWarning

        # Save the cleaned DataFrame to a new CSV file
        df_cleaned.to_csv(args.output, index=False)

        logging.info(f"Suppressed {num_records_suppressed} records.")
        logging.info(f"Cleaned data saved to: {args.output}")

    except FileNotFoundError:
        logging.error(f"Error: File not found: {args.file}")
        sys.exit(1)  # Exit with an error code

    except ValueError as e:
        logging.error(f"Error: {e}")
        sys.exit(1)

    except re.error as e:
        logging.error(f"Error: Invalid regex pattern: {e}")
        sys.exit(1)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        logging.exception(e)  # Log the full traceback for debugging
        sys.exit(1)


if __name__ == "__main__":
    # Usage example:
    # Create a dummy CSV file for testing:
    # echo "Name,SSN,Address" > test.csv
    # echo "John Doe,123-456-7890,123 Main St" >> test.csv
    # echo "Jane Smith,987-654-3210,456 Oak Ave" >> test.csv
    # echo "Peter Jones,No SSN,789 Pine Ln" >> test.csv

    # Run the script:
    # python main.py --file test.csv --column SSN --pattern "\d{3}-\d{3}-\d{4}" --output cleaned.csv

    # Verify the output:
    # cat cleaned.csv # It should contain only the "Peter Jones" record.
    main()