from core.utils import (
    safe_click,
    take_screenshot,
    status,
    debug
)
def select_dropdown(page, label_text, value):
    if value:
        page.get_by_label(label_text, exact=False).select_option(value)
def click_question_radio(page, question_index, answer):
    option = "Yes" if str(answer).lower() == "yes" else "No"

    question_block = page.locator(".question-label").nth(question_index) \
        .locator("xpath=..")  # move to container area

    question_block.get_by_text(option, exact=False).click()

def select_radio_group(page, index, answer):
    option = "Yes" if str(answer).lower() == "yes" else "No"

    group = page.get_by_role("radiogroup").nth(index)

    group.get_by_role("radio", name=option, exact=False).click()

def click_yes_no(page, index, answer):
    option = "Yes" if str(answer).lower() == "yes" else "No"

    # Find question block
    question = page.get_by_role("radiogroup").nth(index)

    # Click Yes / No label
    question.get_by_role("radio", name=option, exact=False).click()

def fill_text_field(page, label_text, value):
    if value:
        page.get_by_label(label_text, exact=False).fill(value)
def fill_vtext_field(page, label_text, value):
    if not value:
        return

    # Click the field container first
    field = page.get_by_text(label_text, exact=False).locator("..").locator("..")
    field.click()

    # Fill the contained input
    field.locator("input").fill(value)
def click_radio_by_question_text(page, question_text, answer):
    option = "Yes" if str(answer).lower() == "yes" else "No"

    # Find question block
    question = page.get_by_text(question_text, exact=False)

    # Move to question container
    container = question.locator("xpath=ancestor::div[contains(@class,'radio-question')]")

    # Click Yes / No label
    container.get_by_label(option, exact=False).click()

def select_named_radio(page, name, answer):
    option = "Yes" if str(answer).lower() == "yes" else "No"

    group = page.locator(f"input[name='{name}']").first.locator("xpath=ancestor::div[contains(@class,'v-input--selection-controls')]")

    group.get_by_label(option, exact=False).click()
     
def select_vselect_option(page, label_text, value):
    # Click field first
    page.get_by_label(label_text, exact=False).click()

    # Wait for menu + click option text
    page.get_by_role("option", name=value, exact=False).click()

def fill_eligibility(page, data):

    try:
        page.wait_for_selector("text=Patient Residence State", timeout=20000)
    except:
        return status(
            "PAGE_LOAD_TIMEOUT",
            "Eligibility page did not load",
            page="eligibility",
            step="wait_for_page"
        )

    patient = data.get("patient_information", {})
    address = patient.get("address", {})
    eligibility = data["eligibility"]
    facility = data.get("facility_information", {})

    try:
    
        select_vselect_option(
            page,
            "Patient Residence State",
            address.get("state")
        )

        select_vselect_option(
            page,
            "Enrollment Site Type",
            "Physician Office"
        )

        # --- v-text-field inputs ---
        fill_vtext_field(page, "Enrollment Site Name", facility.get("name"))
        fill_vtext_field(page, "Enrollment Site Phone Number", facility.get("phone"))
        fill_vtext_field(page, "Enrollment Site Fax Number", facility.get("fax"))

    except Exception as e:
        return status(
            "MISSING_PORTAL_FIELD",
            f"Eligibility field failure: {str(e)}",
            page="eligibility",
            step="field_mapping",
            extra=str(e)
        )


    try:
        groups = page.get_by_role("radio").all_text_contents()
        print("[DEBUG] Radios detected:", groups)
   
        debug("Selecting Q1 — Age ≥ 17")
        click_question_radio(page, 0, eligibility["is_patient_17_or_older"])

        debug("Selecting Q2 — Prescribed for FDA indication")
        click_question_radio(page, 1, eligibility["prescribed_for_fda_approved_indication"])

        debug("Selecting Q3 — Govt-funded insurance (MUST be No)")
        click_question_radio(page, 2, "No")

        debug("Selecting Q4 — Medicare retiree plan (MUST be No)")
        click_question_radio(page, 3, "No")

        debug("Selecting Q5 — Self-pay or uninsured (MUST be No)")
        click_question_radio(page, 4, "No")

        



    except Exception:
        return status(
            "CLICK_ACTION_FAILED",
            "Eligibility radio option selection failed",
            page="eligibility",
            step="eligibility_questions"
           
        )
    try:
        debug("Checking attestation checkbox")

        attestation = page.locator(
            ".v-input--selection-controls__ripple"
        ).last

        attestation.scroll_into_view_if_needed()
        attestation.click()

    except Exception as e:
        take_screenshot(page, "elig_checkbox_failure")
        return status(
            "CLICK_ACTION_FAILED",
            "Eligibility attestation checkbox not selectable",
            page="eligibility",
            step="attestation_checkbox",
            extra=str(e)
        )
    if "checked" not in page.locator("input[type='checkbox']").last.evaluate("el => el.outerHTML"):
        debug("Fallback: clicking attestation label text")
        page.get_by_text("By submitting this application", exact=False).click()

    take_screenshot(page, "01_eligibility")

    if not safe_click(page, "button:has-text('Next')"):
        return status(
            "CLICK_ACTION_FAILED",
            "Next button failed on eligibility page",
            page="eligibility",
            step="next_click"
        )

    return None  # success — continue pipeline
