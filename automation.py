import json
from playwright.sync_api import sync_playwright

PORTAL_URL = "https://portal.trialcard.com/lundbeck/vyepti/"

def load_patient_data(path="input_data.json"):
    with open(path, "r") as f:
        return json.load(f)

def launch_browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, slow_mo=300)
    context = browser.new_context()
    page = context.new_page()
    return playwright, browser, page

def navigate_to_hcp(page):
    page.goto(PORTAL_URL, timeout=60000)

    page.wait_for_selector("text=Health Care Professional")
    page.click("text=Health Care Professional")

    page.wait_for_load_state("networkidle")
