from core.utils import (
    take_screenshot,
    safe_click,
    status
)

def click_vselect_and_choose(page, label_text, value):
    print(f"[DEBUG] Selecting {label_text} = {value}")

    label = page.get_by_text(label_text, exact=False)
    container = label.locator("xpath=ancestor::*[contains(@class,'v-input')]").first

    caret = container.locator(".v-input__icon--append").first
    caret.click()

    option = page.get_by_role("option", name=value, exact=False).first
    option.wait_for(timeout=8000)
    option.click()


def fill_vtext_field(page, label_text, value):
    if not value:
        return

    field = page.get_by_text(label_text, exact=False).locator("xpath=ancestor::*[contains(@class,'v-input')]")
    field.locator("input").first.fill(value)


def select_radio(page, label_text):
    print(f"[DEBUG] Selecting radio: {label_text}")

    label = page.get_by_text(label_text, exact=False)

    radio_container = label.locator(
        "xpath=ancestor::*[contains(@class,'v-radio')]"
    ).first

    radio_container.click(force=True)


def fill_patient_information(page, data):

    try:
        page.wait_for_selector("text=Patient Information", timeout=10000)
    except:
        return status(
            "PAGE_LOAD_TIMEOUT",
            "Patient Information page did not load",
            page="patient_information",
            step="wait_for_page"
        )

    try:
        patient = data["patient_information"]
        address = patient.get("address", {})

        fill_vtext_field(page, "Patient First Name", patient["first_name"])
        fill_vtext_field(page, "Patient Last Name", patient["last_name"])

        fill_vtext_field(page, "Patient Address Line 1", address.get("line1", ""))
        fill_vtext_field(page, "Patient Address Line 2", address.get("line2", ""))

        fill_vtext_field(page, "Patient ZIP", address.get("zip", ""))
        fill_vtext_field(page, "Patient City", address.get("city", ""))

        click_vselect_and_choose(page, "Patient State", address.get("state"))

        fill_vtext_field(page, "Patient Date of Birth", patient["date_of_birth"])

        click_vselect_and_choose(page, "Patient Gender", patient["gender"])

        fill_vtext_field(page, "Patient Email Address", patient["email"])
        fill_vtext_field(page, "Patient Phone Number", patient["phone"])

        select_radio(page, "Home Phone")

    except Exception as e:
        return status(
            "MISSING_PORTAL_FIELD",
            f"Patient field failure: {str(e)}",
            page="patient_information",
            step="field_mapping"
        )

    take_screenshot(page, "02_patient_information_filled")

    if not safe_click(page, "button:has-text('Next')"):
        return status(
            "CLICK_ACTION_FAILED",
            "Next button failed on Patient page",
            page="patient_information",
            step="next_click"
        )

    page.wait_for_load_state("networkidle")

    return None
