import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from supabase import create_client
import time
import os

def setup_undetected_driver():
    """Initialize and return an undetected Chrome driver"""
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = uc.Chrome(options=options)
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
