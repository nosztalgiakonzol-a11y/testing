import os
import time
from datetime import datetime, timezone
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright
from supabase import create_client

TARGET_URL = os.getenv("TARGET_URL", "https://www.sportfogadas.org:2096/irodak/most")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", "600"))
BOOKMAKER = os.getenv("BOOKMAKER", "mostbet").lower()


def get_final_domain(url: str) -> str:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(1500)
        final_url = page.url
        browser.close()
    return urlparse(final_url).netloc


def update_replace_pattern(supabase, domain: str) -> None:
    payload = {
        "replace_pattern": domain,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    supabase.table("link_formatter_rules").update(payload).eq(
        "bookmaker",
        BOOKMAKER,
    ).execute()


def main() -> None:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("SUPABASE_URL és SUPABASE_KEY környezeti változók szükségesek.")

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    while True:
        domain = get_final_domain(TARGET_URL)
        if domain and "sportfogadas.org" not in domain:
            update_replace_pattern(supabase, domain)
            print(f"[{datetime.now(timezone.utc).isoformat()}] Frissítve: {domain}")
        else:
            print(
                f"[{datetime.now(timezone.utc).isoformat()}] Még sportfogadas.org: {domain}"
            )
        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
