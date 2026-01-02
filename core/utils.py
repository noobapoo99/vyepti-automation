import os
import time
from datetime import datetime
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

# --------------------
# STATUS OUTPUT
# --------------------
def status(code, message, page=None, step=None, extra=None):
    output = {
        "timestamp": datetime.now().isoformat(),
        "status_code": code,
        "message": message,
        "page": page,
        "step": step,
        "extra": extra
    }

    print(output)
    return output

def debug(msg):
    print(f"[DEBUG] {msg}")

# --------------------
# SAFE HELPERS
# --------------------
def wait_for_page_header(page, text):
    page.get_by_text(text, exact=False).wait_for(timeout=10000)


def safe_click(page, selector, retries=2):
    for attempt in range(retries + 1):
        try:
            page.locator(selector).click()
            page.wait_for_load_state("networkidle")
            return True
        except Exception:
            print(f"[CLICK RETRY] {selector} attempt {attempt+1}")
            time.sleep(1)

    print(f"[CLICK FAILED] {selector}")
    return False


def wait_for_and_fill(page, locator, value, timeout=8000):
    try:
        page.locator(locator).wait_for(timeout=timeout)
        page.locator(locator).fill(value)
        return True
    except PlaywrightTimeoutError:
        print(f"[TIMEOUT] Field not found → {locator}")
        return False


# --------------------
# SCREENSHOTS / STOP
# --------------------
def take_screenshot(page, name):
    os.makedirs("screenshots", exist_ok=True)
    page.screenshot(path=f"screenshots/{name}.png")


def stop_before_submit(page):
    take_screenshot(page, "final_form_completed")
    print("⚠️ Stopping before submission — review the form.")
    input("Press Enter to close browser...")
