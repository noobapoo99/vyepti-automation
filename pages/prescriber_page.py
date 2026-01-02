from core.utils import safe_click, take_screenshot, status


def fill_vtext_field(page, label_text, value):
    if not value:
        return

    label = page.get_by_text(label_text, exact=False)

    container = label.locator(
        "xpath=ancestor::*[contains(@class,'v-input')]"
    ).first

    input_box = container.locator("input[type='text']").first
    input_box.wait_for(timeout=5000)

    input_box.click()
    input_box.fill(value)

def click_vselect_and_choose(page, label_text, value):
    print(f"[DEBUG] Selecting {label_text} = {value}")

    label = page.get_by_text(label_text, exact=False)

    container = label.locator(
        "xpath=ancestor::*[contains(@class,'v-input')]"
    ).first

    # Click caret icon (Vuetify way to open menu)
    caret = container.locator(".v-input__icon--append").first
    caret.click()

    # Target ONLY real combobox input
    combo = container.locator("input[role='combobox']").first
    combo.wait_for(timeout=5000)
    combo.fill(value.upper())

    # Wait for dropdown options and select match
    option = page.get_by_role("option", name=value, exact=False).first
    option.wait_for(timeout=8000)
    option.click()


def select_vselect(page, label_text, value):
    if not value:
        return

    value = value.upper()

    field = page.get_by_text(label_text, exact=False).locator("..").locator("input")
    field.click()
    field.fill(value)
    page.keyboard.press("Enter")


def fill_prescriber_information(page, data):

    try:
        page.wait_for_selector("text=Referring Physician Information", timeout=15000)
    except:
        return status(
            "PAGE_LOAD_TIMEOUT",
            "Physician page did not load",
            page="prescriber_information",
            step="wait_for_page"
        )

    try:
        physician = data["prescriber_information"]
        address = physician.get("address", {})

        fill_vtext_field(page, "Physician First Name", physician.get("first_name"))
        fill_vtext_field(page, "Physician Last Name", physician.get("last_name"))

        fill_vtext_field(page, "Physician Address Line 1", address.get("line1"))
        fill_vtext_field(page, "Physician City", address.get("city"))



        fill_vtext_field(page, "Physician ZIP", address.get("zip"))

        fill_vtext_field(page, "Physician Office Number", physician.get("phone"))
        fill_vtext_field(page, "Physician Fax Number", physician.get("fax"))
        click_vselect_and_choose(page, "Physician State", address.get("state"))

        
    except Exception as e:
        return status(
            "MISSING_PORTAL_FIELD",
            f"Physician field failure: {str(e)}",
            page="prescriber_information",
            step="field_mapping"
        )

    take_screenshot(page, "03_prescriber_information_filled")

    if not safe_click(page, "button:has-text('Next')"):
        return status(
            "CLICK_ACTION_FAILED",
            "Next button failed on Physician page",
            page="prescriber_information",
            step="next_click"
        )

    page.wait_for_load_state("networkidle")
    return None
