# ArbifyBeta2 - Undetected Selenium Driver with Sports Betting Automation

This project demonstrates the use of undetected-chromedriver for web scraping and automation, combined with Supabase for data storage. It includes specialized functionality for tracking redirects on sports betting websites.

## Features

- **Undetected Selenium Driver**: Uses undetected-chromedriver to bypass bot detection mechanisms
- **Automatic Chrome Version Detection**: Automatically detects installed Chrome version and uses matching ChromeDriver
- **Chrome Version Compatibility**: Handles Chrome version mismatches (e.g., Chrome 144 in Hungary where 145 is not yet available)
- **Sports Betting Site Automation**: Track redirects from sportfogadas.org and extract links
- **Link Submission**: Submit extracted links to external betting sites (e.g., mostbet)
- **Supabase Integration**: Fetches data from Supabase database
- **Visible Browser**: Runs Chrome with visible window for debugging and monitoring
- **Robust Error Handling**: Comprehensive error handling to prevent crashes

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

3. (Optional) Override Chrome version if automatic detection fails:
   ```
   CHROME_VERSION=144
   ```

**Important**: If you don't configure Supabase credentials, the script will skip the Supabase data fetch and only run the Selenium tests. This is useful for testing the browser automation without requiring a database connection.

## Requirements

- Python 3.7+
- Chrome/Chromium browser installed
- Works on Linux and Windows

## Usage

Run the script:

```bash
python ArbifyBeta2.py
```

The script will:
1. **Track sportfogadas.org redirects**
   - Automatically detect your Chrome version
   - Open sportfogadas.org in a visible browser
   - Track where it redirects to
   - Extract all links from the final page
   - Display redirect chain and extracted links

2. **Fetch data from Supabase**
   - Connect to Supabase database
   - Retrieve betting tips data
   - Display total count of results

3. **Optional: Submit links to external sites**
   - Example code included (commented out)
   - Can submit extracted links to sites like mostbet
   - Customize target URL and input selectors as needed

## Code Configuration

The code includes:
- Chrome configuration for automation with visible browser window
- Automatic Chrome version detection to match ChromeDriver version
- Proper error handling and cleanup with try-finally blocks
- Environment variable support for secure credential management
- Explicit waits for reliable page load detection
- Supabase authentication and data fetching

## Chrome Version Handling

The script automatically detects your installed Chrome version and downloads the matching ChromeDriver. This solves the common issue where ChromeDriver version 145 is used but Chrome version 144 is installed (common in Hungary and other regions where latest Chrome versions may not be immediately available).

The detection works on both Linux and Windows:
- **Linux**: Checks `google-chrome --version` or `chromium-browser --version`
- **Windows**: Checks registry (`HKEY_CURRENT_USER\SOFTWARE\Google\Chrome\BLBeacon`) or Chrome executable paths

If automatic detection fails, the script defaults to Chrome version 144 to ensure compatibility in regions where Chrome 145 is not yet available. You can override this default by setting the `CHROME_VERSION` environment variable.

## Functions

- `get_chrome_version()`: Automatically detects the installed Chrome version
- `setup_undetected_driver()`: Initializes and configures the undetected Chrome driver with version matching and stability options
- `track_redirect_and_extract_link()`: Opens a URL, tracks redirects, and extracts links from the final page
- `open_sportfogadas_and_track()`: Main function for sports betting site automation - opens sportfogadas.org and tracks redirects
- `submit_link_to_external_site()`: Submits extracted links to external websites
- `fetch_data_from_supabase()`: Fetches data from Supabase database

## Stability Features

The script includes multiple stability improvements to prevent crashes:

1. **Browser Options**:
   - `--disable-gpu`: Prevents GPU-related crashes
   - `--disable-software-rasterizer`: Improves rendering stability
   - `--disable-extensions`: Prevents extension conflicts
   - `--disable-popup-blocking`: Allows popups for redirect tracking
   - `--ignore-certificate-errors`: Handles SSL certificate issues
   - `--disable-blink-features=AutomationControlled`: Better bot detection avoidance

2. **Timeout Management**:
   - Page load timeout: 30 seconds
   - Script timeout: 30 seconds
   - Explicit waits for page elements
   - Proper cleanup in finally blocks

3. **Error Handling**:
   - Try-except blocks for all network operations
   - Graceful degradation on failures
   - Detailed error logging
   - Clean exit handling

## Example Output

```
======================================================================
TEST 1: Opening sportfogadas.org and tracking redirects
======================================================================
Using Chrome version: 144

[INFO] Opening initial URL: https://www.sportfogadas.org
[INFO] Redirected to: https://www.example-betting-site.com/hu
[INFO] Extracted 45 unique links from the page

[RESULTS]
  Initial URL: https://www.sportfogadas.org
  Final URL: https://www.example-betting-site.com/hu
  Redirect chain: https://www.sportfogadas.org -> https://www.example-betting-site.com/hu
  Total links extracted: 45

[SAMPLE LINKS] (first 5):
    - https://www.example-betting-site.com/sports
    - https://www.example-betting-site.com/live
    - https://www.example-betting-site.com/casino
    ...

======================================================================
TEST 2: Fetching Data from Supabase
======================================================================
Összes találat: 76

======================================================================
All tests completed successfully!
======================================================================
```

## Notes

- The driver runs with a visible browser window for debugging and monitoring
- Proper cleanup is ensured with try-finally blocks
- The code handles exceptions gracefully
- Chrome version is automatically detected and matched with compatible ChromeDriver
- If Chrome version detection fails, defaults to version 144 (for Hungary and similar regions)
- All network operations have timeout protection to prevent hanging

## Recommendations & Best Practices

### 1. **Rate Limiting**
   - Add delays between requests to avoid overloading target sites
   - Consider using `time.sleep()` between operations
   - Respect robots.txt and site terms of service

### 2. **Data Validation**
   - Always validate extracted links before using them
   - Check for valid URL format
   - Filter out unwanted protocols (javascript:, mailto:, etc.)

### 3. **Error Recovery**
   - Implement retry logic for network failures
   - Log errors to files for debugging
   - Consider using a queue system for link processing

### 4. **Security**
   - Never hardcode sensitive credentials (remove before production)
   - Use environment variables for all secrets
   - Implement proper authentication for API access

### 5. **Performance**
   - Consider running in headless mode for production (remove `--headless` removal)
   - Use browser profiles to cache sessions
   - Implement parallel processing for multiple links

### 6. **Monitoring**
   - Add logging to track script execution
   - Monitor for changes in target site structure
   - Set up alerts for repeated failures

### 7. **Legal Compliance**
   - Ensure you have permission to scrape target websites
   - Comply with GDPR and data protection regulations
   - Check gambling/betting regulations in your jurisdiction

### 8. **Customization Tips**
   - Modify `input_selector` in `submit_link_to_external_site()` for specific sites
   - Adjust timeouts based on your network speed
   - Add more specific link filtering in `track_redirect_and_extract_link()`

### 9. **Troubleshooting**
   - If browser crashes: Increase timeout values
   - If redirects not tracked: Check JavaScript execution timing
   - If links not found: Inspect page source for correct selectors
   - If certificate errors: Ensure `--ignore-certificate-errors` is enabled

### 10. **Future Improvements**
   - Add support for multiple betting sites
   - Implement database storage for extracted links
   - Create a web interface for easier operation
   - Add automated scheduling (cron jobs)
   - Implement machine learning for link classification
