import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from supabase import create_client
import time
import os
import subprocess
import re
import sys
import atexit

# TODO: TEMPORARY HARDCODED KEYS FOR TESTING - WILL BE REMOVED TOMORROW
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNvbnVkZ3l5dnhuY2RjZ2FucHBsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDAzMDk0MywiZXhwIjoyMDc1NjA2OTQzfQ.6mmHZJ2QS3a4TywxZ-lswdcvwPCF5NCYLe6CuiO8-3A"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNvbnVkZ3l5dnhuY2RjZ2FucHBsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwMzA5NDMsImV4cCI6MjA3NTYwNjk0M30.QhtBEhUYoZU8dukJ2bNcy95bXW7unxln8NPe_13eBQ4"

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
    
    try:
        # Try to get Chrome version on Windows using registry
        if os.name == 'nt':
            import winreg
            key_path = r'SOFTWARE\Google\Chrome\BLBeacon'
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
            version, _ = winreg.QueryValueEx(key, 'version')
            winreg.CloseKey(key)
            version_match = re.search(r'(\d+)\.', version)
            if version_match:
                return int(version_match.group(1))
    except Exception:
        pass
    
    try:
        # Try Windows Chrome via command line
        if os.name == 'nt':
            chrome_paths = [
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
            ]
            for chrome_path in chrome_paths:
                if os.path.exists(chrome_path):
                    result = subprocess.run([chrome_path, '--version'], 
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        version_match = re.search(r'(\d+)\.', result.stdout)
                        if version_match:
                            return int(version_match.group(1))
    except Exception:
        pass
    
    # Default to version 144 for Hungary where Chrome 145 is not yet available
    # This can be overridden via CHROME_VERSION environment variable
    default_version = int(os.environ.get('CHROME_VERSION', '144'))
    return default_version

def setup_undetected_driver():
    """Initialize and return an undetected Chrome driver with proper version handling"""
    options = uc.ChromeOptions()
    # Headless mode removed to show browser window
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
            try:
                driver.quit()
            except Exception:
                # Suppress any errors during cleanup
                pass

def fetch_data_from_supabase():
    """Fetch data from Supabase database"""
    url = os.environ.get('SUPABASE_URL', 'https://sonudgyyvxncdcganppl.supabase.co')
    # TODO: TEMPORARY - Using hardcoded key for testing, will be removed tomorrow
    key = os.environ.get('SUPABASE_KEY', SUPABASE_SERVICE_KEY)
    
    # Check if valid credentials are provided
    if key == '******':
        print("Warning: Supabase key not configured. Please set SUPABASE_KEY environment variable.")
        print("Skipping Supabase data fetch.")
        return None
    
    supabase = None
    try:
        supabase = create_client(url, key)
        response = supabase.table("tips").select("id, match_name, profit_percent").execute()
        
        print(f"Összes találat: {len(response.data)}")
        return response.data
    except Exception as e:
        print(f"Error fetching data from Supabase: {str(e)}")
        print("Please check your SUPABASE_URL and SUPABASE_KEY environment variables.")
        return None
    finally:
        # Ensure Supabase client resources are cleaned up
        if supabase:
            try:
                # Close any open connections
                if hasattr(supabase, 'postgrest') and hasattr(supabase.postgrest, 'session'):
                    supabase.postgrest.session.close()
            except Exception:
                pass

if __name__ == "__main__":
    try:
        print("=== Testing Undetected Selenium Driver ===")
        fetch_data_with_selenium()
        
        print("\n=== Fetching Data from Supabase ===")
        fetch_data_from_supabase()
        
        # Allow time for proper cleanup
        print("\nScript completed successfully!")
        time.sleep(0.5)
        
    except KeyboardInterrupt:
        print("\nScript interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        sys.exit(1)
    finally:
        # Ensure clean exit
        sys.exit(0)
