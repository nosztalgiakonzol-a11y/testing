import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from supabase import create_client
import time
import os
import subprocess
import re

def get_chrome_version():
    """
    Detect the installed Chrome version.
    
    Returns:
        int: The major version number of installed Chrome (e.g., 144).
             Defaults to 144 if detection fails (for regions like Hungary 
             where Chrome 145 is not yet available).
    """
    try:
        # Try to get Chrome version on Linux
        result = subprocess.run(['google-chrome', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version_match = re.search(r'(\d+)\.', result.stdout)
            if version_match:
                return int(version_match.group(1))
    except (FileNotFoundError, subprocess.SubprocessError, subprocess.TimeoutExpired):
        pass
    
    try:
        # Try alternative command
        result = subprocess.run(['chromium-browser', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version_match = re.search(r'(\d+)\.', result.stdout)
            if version_match:
                return int(version_match.group(1))
    except (FileNotFoundError, subprocess.SubprocessError, subprocess.TimeoutExpired):
        pass
    
    # Default to version 144 for Hungary where Chrome 145 is not yet available
    # This can be overridden via CHROME_VERSION environment variable
    default_version = int(os.environ.get('CHROME_VERSION', '144'))
    return default_version

def setup_undetected_driver():
    """Initialize and return an undetected Chrome driver with proper version handling"""
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Get the Chrome version to use the matching ChromeDriver
    chrome_version = get_chrome_version()
    print(f"Using Chrome version: {chrome_version}")
    
    # Create driver with specified Chrome version
    # This ensures ChromeDriver matches the installed Chrome version
    driver = uc.Chrome(options=options, version_main=chrome_version)
    return driver

def fetch_data_with_selenium():
    """Fetch data using undetected selenium driver"""
    driver = None
    try:
        driver = setup_undetected_driver()
        
        # Example: Navigate to Supabase or any website
        url = "https://sonudgyyvxncdcganppl.supabase.co"
        driver.get(url)
        
        # Wait for page to load using explicit wait
        wait = WebDriverWait(driver, 10)
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
        
        print(f"Successfully loaded page: {driver.title}")
        print(f"Current URL: {driver.current_url}")
        
        return True
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return False
    finally:
        if driver:
            driver.quit()

def fetch_data_from_supabase():
    """Fetch data from Supabase database"""
    url = os.environ.get('SUPABASE_URL', 'https://sonudgyyvxncdcganppl.supabase.co')
    key = os.environ.get('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNvbnVkZ3l5dnhuY2RjZ2FucHBsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDAzMDk0MywiZXhwIjoyMDc1NjA2OTQzfQ.6mmHZJ2QS3a4TywxZ-lswdcvwPCF5NCYLe6CuiO8-3A')
    
    supabase = create_client(url, key)
    response = supabase.table("tips").select("id, match_name, profit_percent").execute()
    
    print(f"Összes találat: {len(response.data)}")
    return response.data

if __name__ == "__main__":
    print("=== Testing Undetected Selenium Driver ===")
    fetch_data_with_selenium()
    
    print("\n=== Fetching Data from Supabase ===")
    fetch_data_from_supabase()
