from core.utils import (
    safe_click,
    take_screenshot,
    status
)

def fill_prescriber_information(page, data):

    try:
        page.wait_for_selector("text=Referring Physician Information", timeout=10000)
    except:
        return status(
            "PAGE_LOAD_TIMEOUT",
            "Physician page did not load",
            page="prescriber_information",
            step="wait_for_page"
        )

    try:
        page.fill("input[name='PhysicianFirstName']", data["first_name"])
        page.fill("input[name='PhysicianLastName']", data["last_name"])

        page.fill("input[name='PhysicianAddress1']", data["address"]["line1"])
        page.fill("input[name='PhysicianCity']", data["address"]["city"])

        page.locator("select[name='PhysicianState']").select_option(
            label=data["address"]["state"]
        )

        page.fill("input[name='PhysicianZIP']", data["address"]["zip"])

        page.fill("input[name='PhysicianOfficeNumber']", data["phone"])
        page.fill("input[name='PhysicianFaxNumber']", data["fax"])

    except Exception as e:
        return status(
            "MISSING_PORTAL_FIELD",
            f"Physician field failure: {str(e)}",
            page="prescriber_information",
            step="field_mapping"
        )

    take_screenshot(page, "03_physician_information_filled")

    if not safe_click(page, "button:has-text('Next')"):
        return status(
            "CLICK_ACTION_FAILED",
            "Next button failed on Physician page",
            page="prescriber_information",
            step="next_click"
        )

    page.wait_for_load_state("networkidle")

    return None  # success
