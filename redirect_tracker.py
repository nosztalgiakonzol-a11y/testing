"""
Simple Redirect Tracker
Megnyit egy URL-t a böngészőben, követi a redirectet, és kiírja a végső URL-t.
"""

import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
import subprocess
import re

def get_chrome_version():
    """Chrome verzió detektálása"""
    try:
        # Windows
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
        # Linux
        result = subprocess.run(['google-chrome', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version_match = re.search(r'(\d+)\.', result.stdout)
            if version_match:
                return int(version_match.group(1))
    except Exception:
        pass
    
    # Default
    return int(os.environ.get('CHROME_VERSION', '144'))

def setup_driver():
    """Chrome driver beállítása"""
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    chrome_version = get_chrome_version()
    print(f"Chrome verzió: {chrome_version}")
    
    driver = uc.Chrome(options=options, version_main=chrome_version)
    driver.set_page_load_timeout(30)
    
    return driver

def get_final_url(url):
    """
    Megnyit egy URL-t, követi a redirectet, és visszaadja a végső URL-t
    
    Args:
        url: A kezdő URL
    
    Returns:
        str: A végső URL a redirect után
    """
    driver = None
    try:
        print(f"\n{'='*70}")
        print(f"Kezdő URL: {url}")
        print('='*70)
        
        driver = setup_driver()
        
        # URL megnyitása
        print("Böngésző megnyitása...")
        driver.get(url)
        
        # Várunk a betöltésre
        wait = WebDriverWait(driver, 30)
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
        
        # Kis várakozás a JavaScript redirect-ekre
        time.sleep(3)
        
        # Végső URL lekérése
        final_url = driver.current_url
        
        print(f"\n✓ VÉGSŐ URL: {final_url}")
        print('='*70)
        
        return final_url
        
    except Exception as e:
        print(f"\n✗ HIBA: {str(e)}")
        return None
        
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def main():
    """Fő program"""
    print("\n" + "="*70)
    print("REDIRECT TRACKER - Egyszerű verzió")
    print("="*70)
    
    # A két teszt URL
    urls = [
        "http://boabet.com/hu",
        "https://www.sportfogadas.org:2096/irodak/most"
    ]
    
    results = []
    
    # Minden URL feldolgozása
    for url in urls:
        final_url = get_final_url(url)
        if final_url:
            results.append({
                'original': url,
                'final': final_url
            })
        
        # Kis szünet két kérés között
        time.sleep(2)
    
    # Eredmények összefoglalása
    print("\n" + "="*70)
    print("ÖSSZEFOGLALÓ")
    print("="*70)
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Oldal:")
        print(f"   Kezdő:  {result['original']}")
        print(f"   Végső:  {result['final']}")
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
