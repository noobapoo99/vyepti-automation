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

def select_yes_no(page, label_text, value):
    option = "Yes" if value.lower() == "yes" else "No"
    page.get_by_label(label_text).check()

def fill_eligibility(page, eligibility):
    page.wait_for_selector("text=Is your patient 17 years of age or older?")

    mappings = [
        ("Is your patient 17 years of age or older?",
         eligibility["is_patient_17_or_older"]),
        ("Has your patient been prescribed VYEPTI for an FDA-approved indication?",
         eligibility["prescribed_for_fda_approved_indication"]),
        ("Is your patient enrolled in a state or federally-funded health insurance program",
         "No"),  # must be NO
        ("Is your patient self-pay or uninsured?",
         "No"),  # must be NO
    ]

    for label, val in mappings:
        option = "Yes" if val.lower() == "yes" else "No"
        page.get_by_label(option, exact=True).check()

    page.screenshot(path="screenshots/01_eligibility.png")
    page.click("text=NEXT")
    page.wait_for_load_state("networkidle")

def fill_patient_information(page, patient):
    page.wait_for_selector("text=Patient Information")

    page.fill("input[name='PatientFirstName']", patient["first_name"])
    page.fill("input[name='PatientLastName']", patient["last_name"])

    page.fill("input[name='PatientAddress1']", patient["address"]["line1"])
    page.fill("input[name='PatientCity']", patient["address"]["city"])

    page.select_option("select[name='PatientState']", patient["address"]["state"])
    page.fill("input[name='PatientZIP']", patient["address"]["zip"])

    page.select_option("select[name='PatientGender']", patient["gender"])
    page.fill("input[name='PatientDOB']", patient["date_of_birth"])

    page.fill("input[name='PatientEmail']", patient["email"])
    page.fill("input[name='PatientPhone']", patient["phone"])

    page.screenshot(path="screenshots/02_patient_information.png")
    page.click("text=NEXT")
    page.wait_for_load_state("networkidle")

def fill_prescriber_information(page, prescriber):
    page.wait_for_selector("text=Referring Physician Information")

    page.fill("input[name='PhysicianFirstName']", prescriber["first_name"])
    page.fill("input[name='PhysicianLastName']", prescriber["last_name"])

    page.fill("input[name='PhysicianAddress1']", prescriber["address"]["line1"])
    page.fill("input[name='PhysicianCity']", prescriber["address"]["city"])
    page.select_option("select[name='PhysicianState']", prescriber["address"]["state"])
    page.fill("input[name='PhysicianZIP']", prescriber["address"]["zip"])

    page.fill("input[name='PhysicianOfficeNumber']", prescriber["phone"])
    page.fill("input[name='PhysicianFaxNumber']", prescriber["fax"])

    page.screenshot(path="screenshots/03_physician_information.png")
    page.click("text=NEXT")
    page.wait_for_load_state("networkidle")

def fill_primary_insurance(page, insurance):
    page.wait_for_selector("text=Insurance Information")

    page.select_option("select[name='InsuranceState']", "ILLINOIS")  # or from JSON
    page.fill("input[name='InsuranceCarrier']", insurance["insurance_name"])

    holder = insurance["policy_holder_name"].split(" ", 1)
    page.fill("input[name='PolicyHolderFirstName']", holder[0])
    page.fill("input[name='PolicyHolderLastName']", holder[1])

    page.fill("input[name='PolicyNumber']", insurance["member_id"])
    page.fill("input[name='GroupNumber']", insurance["group_id"])

    # Signature field (type full name)
    page.fill("input[name='SignatureName']", holder[0].lower() + " " + holder[1].lower())

    page.screenshot(path="screenshots/04_insurance_filled.png")

    print("⚠️ STOPPING BEFORE ENROLL — submission disabled.")
    input("Press Enter to close browser...")

def run_enrollment_flow(page, data):

    fill_eligibility(page, data["eligibility"])
    fill_patient_information(page, data["patient_information"])
    fill_prescriber_information(page, data["prescriber_information"])
    fill_primary_insurance(page, data["primary_insurance"])

    return {
        "status_code": "SUCCESS_FORM_COMPLETED",
        "message": "All pages filled — stopped before submission"
    }
