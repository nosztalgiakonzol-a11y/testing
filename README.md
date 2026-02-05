# ArbifyBeta2 - Undetected Selenium Driver

This project demonstrates the use of undetected-chromedriver for web scraping and automation, combined with Supabase for data storage.

## Features

- **Undetected Selenium Driver**: Uses undetected-chromedriver to bypass bot detection mechanisms
- **Supabase Integration**: Fetches data from Supabase database
- **Headless Mode**: Runs Chrome in headless mode for automation

## Installation

```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.7+
- Chrome/Chromium browser installed

## Usage

Run the script:

```bash
python ArbifyBeta2.py
```

The script will:
1. Initialize an undetected Chrome driver
2. Navigate to a specified URL
3. Fetch data from Supabase database

## Configuration

The code includes:
- Headless Chrome configuration
- Proper error handling and cleanup
- Supabase authentication and data fetching

## Functions

- `setup_undetected_driver()`: Initializes and configures the undetected Chrome driver
- `fetch_data_with_selenium()`: Demonstrates web navigation using undetected selenium
- `fetch_data_from_supabase()`: Fetches data from Supabase database

## Notes

- The driver runs in headless mode for better performance in automated environments
- Proper cleanup is ensured with try-finally blocks
- The code handles exceptions gracefully
