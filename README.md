# ArbifyBeta2 - Undetected Selenium Driver

This project demonstrates the use of undetected-chromedriver for web scraping and automation, combined with Supabase for data storage.

## Features

- **Undetected Selenium Driver**: Uses undetected-chromedriver to bypass bot detection mechanisms
- **Automatic Chrome Version Detection**: Automatically detects installed Chrome version and uses matching ChromeDriver
- **Chrome Version Compatibility**: Handles Chrome version mismatches (e.g., Chrome 144 in Hungary where 145 is not yet available)
- **Supabase Integration**: Fetches data from Supabase database
- **Headless Mode**: Runs Chrome in headless mode for automation

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Supabase credentials:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-service-role-key-here
   ```

Note: The code will fall back to default values if environment variables are not set, but it's recommended to use environment variables for security.

## Requirements

- Python 3.7+
- Chrome/Chromium browser installed

## Usage

Run the script:

```bash
python ArbifyBeta2.py
```

The script will:
1. Automatically detect your Chrome version
2. Initialize an undetected Chrome driver with matching ChromeDriver version
3. Navigate to a specified URL
4. Fetch data from Supabase database

## Code Configuration

The code includes:
- Headless Chrome configuration for automation
- Automatic Chrome version detection to match ChromeDriver version
- Proper error handling and cleanup with try-finally blocks
- Environment variable support for secure credential management
- Explicit waits for reliable page load detection
- Supabase authentication and data fetching

## Chrome Version Handling

The script automatically detects your installed Chrome version and downloads the matching ChromeDriver. This solves the common issue where ChromeDriver version 145 is used but Chrome version 144 is installed (common in Hungary and other regions where latest Chrome versions may not be immediately available).

If automatic detection fails, the script defaults to Chrome version 144 to ensure compatibility in regions where Chrome 145 is not yet available.

## Functions

- `get_chrome_version()`: Automatically detects the installed Chrome version
- `setup_undetected_driver()`: Initializes and configures the undetected Chrome driver with version matching
- `fetch_data_with_selenium()`: Demonstrates web navigation using undetected selenium
- `fetch_data_from_supabase()`: Fetches data from Supabase database

## Notes

- The driver runs in headless mode for better performance in automated environments
- Proper cleanup is ensured with try-finally blocks
- The code handles exceptions gracefully
- Chrome version is automatically detected and matched with compatible ChromeDriver
- If Chrome version detection fails, defaults to version 144 (for Hungary and similar regions)
