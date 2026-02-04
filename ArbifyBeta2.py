import os
import time
from datetime import datetime, timezone
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright
from supabase import create_client

TARGET_URL = os.getenv("TARGET_URL", "https://www.sportfogadas.org:2096/irodak/most")
BOABET_URL = os.getenv("BOABET_URL", "https://boabet.com/hu")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", "600"))
MAX_LOAD_SECONDS = int(os.getenv("MAX_LOAD_SECONDS", "120"))
NAVIGATION_RETRIES = int(os.getenv("NAVIGATION_RETRIES", "2"))
BOOKMAKER = os.getenv("BOOKMAKER", "mostbet").lower()
BOABET_BOOKMAKER = os.getenv("BOABET_BOOKMAKER", "boabet").lower()
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
BLOCK_RESOURCES = os.getenv("BLOCK_RESOURCES", "true").lower() == "true"
VEGAS_BOOKMAKER = os.getenv("VEGAS_BOOKMAKER", "vegas").lower()
VEGAS_CHECK_ENABLED = os.getenv("VEGAS_CHECK_ENABLED", "true").lower() == "true"
VEGAS_TEXT = os.getenv(
    "VEGAS_TEXT",
    "Ez az esemény lezárult. Kérjük, nézze meg a többi elérhető eseményt.",
)
VEGAS_POLL_LIMIT = int(os.getenv("VEGAS_POLL_LIMIT", "25"))


def navigate_and_capture(browser, url: str) -> tuple[str, str]:
    context = browser.new_context()
    if BLOCK_RESOURCES:
        context.route(
            "**/*",
            lambda route: route.abort()
            if route.request.resource_type in {"image", "media", "font"}
            else route.continue_(),
        )
    page = context.new_page()
    final_url = ""
    content = ""
    for attempt in range(1, NAVIGATION_RETRIES + 1):
        try:
            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=MAX_LOAD_SECONDS * 1000,
            )
            page.wait_for_timeout(1500)
            final_url = page.url
            content = page.content()
            break
        except Exception as exc:
            print(f"Hiba a navigációban (próbálkozás {attempt}): {exc}")
    context.close()
    return final_url, content


def get_final_domain(browser, url: str) -> str:
    final_url, _ = navigate_and_capture(browser, url)
    return urlparse(final_url).netloc if final_url else ""


def update_replace_pattern(supabase, bookmaker: str, domain: str) -> None:
    payload = {
        "replace_pattern": domain,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    supabase.table("link_formatter_rules").update(payload).eq(
        "bookmaker",
        bookmaker,
    ).execute()


def fetch_new_vegas_tips(supabase, last_seen_id: int) -> tuple[int, list[dict]]:
    query = (
        supabase.table("tips")
        .select("id, bookmaker1, bookmaker2, original_link1, original_link2")
        .order("id")
        .limit(VEGAS_POLL_LIMIT)
    )
    if last_seen_id > 0:
        query = query.gt("id", last_seen_id)
    response = query.execute()
    tips = response.data or []
    if tips:
        last_seen_id = max(tip["id"] for tip in tips if "id" in tip)
    return last_seen_id, tips


def check_vegas_tip(browser, page_url: str) -> None:
    final_url, content = navigate_and_capture(browser, page_url)
    if not final_url:
        print(f"[{datetime.now(timezone.utc).isoformat()}] Vegas link nem töltött be.")
        return
    if VEGAS_TEXT in content:
        print(
            f"[{datetime.now(timezone.utc).isoformat()}] Vegas lezárt esemény: {final_url}"
        )
    else:
        print(
            f"[{datetime.now(timezone.utc).isoformat()}] Vegas ellenőrzés OK: {final_url}"
        )


def process_vegas_tips(supabase, browser, last_seen_id: int) -> int:
    last_seen_id, tips = fetch_new_vegas_tips(supabase, last_seen_id)
    if not tips:
        return last_seen_id
    for tip in tips:
        if tip.get("bookmaker1", "").lower() == VEGAS_BOOKMAKER:
            link = tip.get("original_link1")
            if link:
                check_vegas_tip(browser, link)
        if tip.get("bookmaker2", "").lower() == VEGAS_BOOKMAKER:
            link = tip.get("original_link2")
            if link:
                check_vegas_tip(browser, link)
    return last_seen_id


def main() -> None:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("SUPABASE_URL és SUPABASE_KEY környezeti változók szükségesek.")

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    last_seen_id = 0
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=HEADLESS)
        while True:
            domain = get_final_domain(browser, TARGET_URL)
            if not domain:
                print(
                    f"[{datetime.now(timezone.utc).isoformat()}] Nem sikerült domain-t kinyerni."
                )
            elif "sportfogadas.org" not in domain:
                update_replace_pattern(supabase, BOOKMAKER, domain)
                print(f"[{datetime.now(timezone.utc).isoformat()}] Frissítve: {domain}")
            else:
                print(
                    f"[{datetime.now(timezone.utc).isoformat()}] Még sportfogadas.org: {domain}"
                )

            boabet_domain = get_final_domain(browser, BOABET_URL)
            if not boabet_domain:
                print(
                    f"[{datetime.now(timezone.utc).isoformat()}] Nem sikerült boabet domain-t kinyerni."
                )
            elif "boabet.com" not in boabet_domain:
                update_replace_pattern(supabase, BOABET_BOOKMAKER, boabet_domain)
                print(
                    f"[{datetime.now(timezone.utc).isoformat()}] Boabet frissítve: {boabet_domain}"
                )
            else:
                print(
                    f"[{datetime.now(timezone.utc).isoformat()}] Még boabet.com: {boabet_domain}"
                )

            if VEGAS_CHECK_ENABLED:
                last_seen_id = process_vegas_tips(supabase, browser, last_seen_id)

            time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
