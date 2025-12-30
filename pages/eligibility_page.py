from core.utils import take_screenshot

def fill_eligibility(page, data):
    page.wait_for_selector("text=Is your patient 17 years of age or older?")
    mappings = [
        ("Is your patient 17 years of age or older?",
         data["is_patient_17_or_older"]),
        ("Has your patient been prescribed VYEPTI for an FDA-approved indication?",
         data["prescribed_for_fda_approved_indication"]),
        ("Is your patient enrolled in a state or federally-funded health insurance program",
         "No"),  # must be NO
        ("Is your patient self-pay or uninsured?",
         "No"),  # must be NO
    ]

    for label, val in mappings:
        option = "Yes" if val.lower() == "yes" else "No"
        page.get_by_label(option, exact=True).check()
    take_screenshot(page, "./../screenshots01_eligibility")
    page.click("text=NEXT")
    page.wait_for_load_state("networkidle")
