# dat-Record-Suppression
Removes entire records from a dataset if they contain sensitive information identified by a pattern (e.g., SSN regex). Takes pattern and column name as arguments. Uses regex module. - Focused on A collection of utilities for anonymizing sensitive data in datasets. Includes tools for replacing real names, addresses, phone numbers, and other PII with fake but realistic values, while preserving data structure and relationships. Supports various data formats like CSV and JSON.

## Install
`git clone https://github.com/ShadowGuardAI/dat-record-suppression`

## Usage
`./dat-record-suppression [params]`

## Parameters
- `-h`: Show help message and exit
- `--file`: Path to the input CSV file.
- `--column`: Name of the column to check for sensitive information.
- `--pattern`: Regex pattern to identify sensitive information.
- `--output`: Path to the output CSV file.

## License
Copyright (c) ShadowGuardAI
