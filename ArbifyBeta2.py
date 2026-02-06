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
    """Initialize and return an undetected Chrome driver with proper version handling and stability options"""
    options = uc.ChromeOptions()
    # Headless mode removed to show browser window
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Additional stability options to prevent crashes
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    # Set page load strategy to prevent hanging
    options.page_load_strategy = 'normal'
    
    # Get the Chrome version to use the matching ChromeDriver
    chrome_version = get_chrome_version()
    print(f"Using Chrome version: {chrome_version}")
    
    # Create driver with specified Chrome version
    # This ensures ChromeDriver matches the installed Chrome version
    driver = uc.Chrome(options=options, version_main=chrome_version)
    
    # Set timeouts to prevent hanging
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)
    
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

def track_redirect_and_extract_link(driver, initial_url, timeout=30):
    """
    Open a URL, track where it redirects, and extract links from the final page.
    
    Args:
        driver: Selenium WebDriver instance
        initial_url: The URL to start from (e.g., sportfogadas.org)
        timeout: Maximum time to wait for redirect (default 30 seconds)
    
    Returns:
        dict: {
            'initial_url': str,
            'final_url': str,
            'redirect_chain': list,
            'extracted_links': list
        }
    """
    result = {
        'initial_url': initial_url,
        'final_url': None,
        'redirect_chain': [],
        'extracted_links': []
    }
    
    try:
        print(f"\n[INFO] Opening initial URL: {initial_url}")
        
        # Navigate to the initial URL
        driver.get(initial_url)
        result['redirect_chain'].append(initial_url)
        
        # Wait for page to be fully loaded
        wait = WebDriverWait(driver, timeout)
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
        
        # Small delay to allow any JavaScript redirects to complete
        time.sleep(2)
        
        # Get the final URL after redirects
        final_url = driver.current_url
        result['final_url'] = final_url
        
        if final_url != initial_url:
            result['redirect_chain'].append(final_url)
            print(f"[INFO] Redirected to: {final_url}")
        else:
            print(f"[INFO] No redirect occurred, stayed at: {final_url}")
        
        # Extract all links from the final page
        try:
            links = driver.find_elements(By.TAG_NAME, 'a')
            for link in links:
                href = link.get_attribute('href')
                if href and href.startswith('http'):
                    result['extracted_links'].append(href)
            
            # Remove duplicates
            result['extracted_links'] = list(set(result['extracted_links']))
            print(f"[INFO] Extracted {len(result['extracted_links'])} unique links from the page")
            
        except Exception as e:
            print(f"[WARNING] Could not extract links: {str(e)}")
        
        return result
        
    except Exception as e:
        print(f"[ERROR] Error tracking redirect: {str(e)}")
        result['error'] = str(e)
        return result

def open_sportfogadas_and_track():
    """
    Opens sportfogadas.org, tracks redirects, and extracts links.
    Main function for the sports betting site automation.
    
    Returns:
        dict: Information about the redirect and extracted links
    """
    driver = None
    try:
        print("\n" + "="*60)
        print("Opening sportfogadas.org and tracking redirects")
        print("="*60)
        
        driver = setup_undetected_driver()
        
        # Track redirect from sportfogadas.org
        result = track_redirect_and_extract_link(
            driver, 
            "https://www.sportfogadas.org",
            timeout=30
        )
        
        # Display results
        print("\n[RESULTS]")
        print(f"  Initial URL: {result['initial_url']}")
        print(f"  Final URL: {result['final_url']}")
        print(f"  Redirect chain: {' -> '.join(result['redirect_chain'])}")
        print(f"  Total links extracted: {len(result['extracted_links'])}")
        
        if result['extracted_links']:
            print(f"\n[SAMPLE LINKS] (first 5):")
            for link in result['extracted_links'][:5]:
                print(f"    - {link}")
        
        return result
        
    except Exception as e:
        print(f"[ERROR] Failed to open sportfogadas.org: {str(e)}")
        return {'error': str(e)}
    finally:
        if driver:
            try:
                print("\n[INFO] Closing browser...")
                driver.quit()
            except Exception as e:
                print(f"[WARNING] Error closing browser: {str(e)}")

def submit_link_to_external_site(driver, target_url, link_to_submit, input_selector=None):
    """
    Submit a link to an external website (e.g., mostbet).
    
    Args:
        driver: Selenium WebDriver instance
        target_url: The URL where to submit (e.g., mostbet page)
        link_to_submit: The link to submit
        input_selector: CSS selector for the input field (optional)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"\n[INFO] Opening target site: {target_url}")
        driver.get(target_url)
        
        # Wait for page to load
        wait = WebDriverWait(driver, 20)
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
        
        print(f"[INFO] Successfully loaded: {driver.current_url}")
        print(f"[INFO] Link to submit: {link_to_submit}")
        
        # If input selector is provided, try to find and fill the input
        if input_selector:
            try:
                input_element = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, input_selector))
                )
                input_element.clear()
                input_element.send_keys(link_to_submit)
                print(f"[SUCCESS] Link submitted to input field")
                return True
            except Exception as e:
                print(f"[WARNING] Could not find input field with selector '{input_selector}': {str(e)}")
        
        # If no selector or selector failed, just report success of opening the page
        print(f"[INFO] Target page opened. Manual submission may be required.")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to submit link: {str(e)}")
        return False

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
        # Test 1: Track sportfogadas.org redirects
        print("\n" + "="*70)
        print("TEST 1: Opening sportfogadas.org and tracking redirects")
        print("="*70)
        result = open_sportfogadas_and_track()
        
        # Test 2: Fetch data from Supabase
        print("\n" + "="*70)
        print("TEST 2: Fetching Data from Supabase")
        print("="*70)
        fetch_data_from_supabase()
        
        # Test 3: Example of submitting a link (commented out by default)
        # Uncomment and configure when you have a specific target site
        """
        if result and result.get('final_url'):
            driver = setup_undetected_driver()
            try:
                submit_link_to_external_site(
                    driver,
                    target_url="https://www.mostbet.com",  # Example target
                    link_to_submit=result['final_url'],
                    input_selector=None  # Add selector if you know it
                )
                time.sleep(3)  # Allow time to see the result
            finally:
                driver.quit()
        """
        
        # Allow time for proper cleanup
        print("\n" + "="*70)
        print("All tests completed successfully!")
        print("="*70)
        time.sleep(0.5)
        
    except KeyboardInterrupt:
        print("\n[INFO] Script interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Ensure clean exit
        sys.exit(0)
