from core.utils import (
    take_screenshot,
    stop_before_submit,
    status
)

def fill_vtext_field(page, label_text, value):
    if not value:
        return

    label = page.get_by_text(label_text, exact=False)
    container = label.locator("xpath=ancestor::*[contains(@class,'v-input')]").first
    input_box = container.locator("input[type='text']").first
    input_box.wait_for(timeout=5000)
    input_box.click()
    input_box.fill(value)


def click_vselect_and_choose(page, label_text, value):
    if not value:
        return

    label = page.get_by_text(label_text, exact=False)
    container = label.locator("xpath=ancestor::*[contains(@class,'v-input')]").first
    caret = container.locator(".v-input__icon--append").first
    caret.click()

    option = page.get_by_role("option", name=value, exact=False).first
    option.wait_for(timeout=8000)
    option.click()


def fill_primary_insurance(page, data):
    try:
        page.wait_for_selector("text=Insurance Information", timeout=10000)
    except:
        return status(
            "PAGE_LOAD_TIMEOUT",
            "Insurance page did not load",
            page="insurance_information",
            step="wait_for_page"
        )

    try:
        insurance = data.get("primary_insurance")

        if not insurance:
            page.get_by_label("Patient does not have Medical insurance").click()
            take_screenshot(page, "04_insurance_skipped_no_insurance")
            return stop_before_submit(page)

        click_vselect_and_choose(
            page,
            "Insurance State",
            insurance.get("state", "ALABAMA")
        )

        click_vselect_and_choose(
            page,
            "Insurance Carrier",
            insurance.get("insurance_name")
        )

        holder_first, holder_last = insurance["policy_holder_name"].split(" ", 1)

        fill_vtext_field(page, "Policy Holder First Name", holder_first)
        fill_vtext_field(page, "Policy Holder Last Name", holder_last)
        fill_vtext_field(page, "Policy Number", insurance.get("member_id"))
        fill_vtext_field(page, "Group Number", insurance.get("group_id"))

        if insurance.get("has_secondary", False):
            page.get_by_label("Patient has secondary Medical insurance.").click()

    except Exception as e:
        return status(
            "MISSING_PORTAL_FIELD",
            f"Insurance field failure: {str(e)}",
            page="insurance_information",
            step="field_mapping"
        )

    take_screenshot(page, "04_insurance_information_filled")

    return stop_before_submit(page)
