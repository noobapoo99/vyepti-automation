import json
from core.browser import start_browser
from pages.eligibility_page import fill_eligibility
from pages.patient_page import fill_patient_information
from pages.prescriber_page import fill_prescriber_information
from pages.insurance_page import fill_primary_insurance
from core.utils import status

PORTAL_URL = "https://portal.trialcard.com/lundbeck/vyepti/"

def load_data():
    with open("data/input_data.json") as f:
        return json.load(f)

def main():
    browser = None

    try:
        data = load_data()

        pw, browser, page = start_browser()

        page.goto(PORTAL_URL)

        fill_eligibility(page, data["eligibility"])
        fill_patient_information(page, data["patient_information"])
        fill_prescriber_information(page, data["prescriber_information"])
        fill_primary_insurance(page, data["primary_insurance"])

        status("SUCCESS_FORM_COMPLETED",
               "All pages completed — stopped before submission")

    except Exception as e:
        status("UNKNOWN_ERROR", str(e))

    finally:
        if browser:
            browser.close()

if __name__ == "__main__":
    main()
