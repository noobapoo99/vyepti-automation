from playwright.sync_api import sync_playwright

def start_browser(headless=False, slow_mo=300):
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=headless, slow_mo=slow_mo)
    context = browser.new_context()
    page = context.new_page()
    return pw, browser, page
