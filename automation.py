import json
from core.browser import start_browser
from pages.eligibility_page import fill_eligibility
from pages.patient_page import fill_patient_information
from pages.prescriber_page import fill_prescriber_information
from pages.insurance_page import fill_primary_insurance
from core.utils import status
from pages.start_page import enter_hcp_portal

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
        result = enter_hcp_portal(page)
        if result:
            return result
    
        # ---- PAGE 1 ----
        result = fill_eligibility(page, data)
        if result:
            return result

        # ---- PAGE 2 ----
        result = fill_patient_information(page, data)
        if result:
            return result

        # ---- PAGE 3 ----
        result = fill_prescriber_information(page, data)
        if result:
            return result

        # ---- PAGE 4 (STOP HERE) ----
        result = fill_primary_insurance(page, data)
        if result:
            return result

        return status(
            "SUCCESS_FORM_COMPLETED",
            "All pages completed — stopped before submission",
            step="stop_before_submit",
            page="insurance_information"
        )

    except KeyError:
        return status(
            "INVALID_JSON_STRUCTURE",
            "Missing required JSON fields",
            step="precheck"
        )

    except Exception as e:
        return status(
            "UNKNOWN_ERROR",
            str(e),
            step="runtime"
        )

    finally:
        if browser:
            browser.close()

if __name__ == "__main__":
    main()
