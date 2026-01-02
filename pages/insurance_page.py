from core.utils import (
    take_screenshot,
    stop_before_submit,
    status
)

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
        page.select_option("select[name='InsuranceState']", "ILLINOIS")

        page.fill("input[name='InsuranceCarrier']", data["insurance_name"])

        holder_first, holder_last = data["policy_holder_name"].split(" ", 1)

        page.fill("input[name='PolicyHolderFirstName']", holder_first)
        page.fill("input[name='PolicyHolderLastName']", holder_last)

        page.fill("input[name='PolicyNumber']", data["member_id"])
        page.fill("input[name='GroupNumber']", data["group_id"])

    except Exception as e:
        return status(
            "MISSING_PORTAL_FIELD",
            f"Insurance field failure: {str(e)}",
            page="insurance_information",
            step="field_mapping"
        )

    take_screenshot(page, "04_insurance_information_filled")

    # REQUIRED BY ASSIGNMENT — STOP HERE
    return stop_before_submit(page)
