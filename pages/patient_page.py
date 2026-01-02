from core.utils import (
    take_screenshot,
    safe_click,
    status
)

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

        page.fill("input[name='PatientFirstName']", patient["first_name"])
        page.fill("input[name='PatientLastName']", patient["last_name"])

        page.fill("input[name='PatientAddress1']", address.get("line1", ""))
        page.fill("input[name='PatientCity']", address.get("city", ""))

        page.locator("select[name='PatientState']").select_option(
            label=address.get("state", "")
        )

        page.fill("input[name='PatientZIP']", address.get("zip", ""))

        page.locator("select[name='PatientGender']").select_option(
            label=patient["gender"]
        )

        page.fill("input[name='PatientDOB']", patient["date_of_birth"])
        page.fill("input[name='PatientEmail']", patient["email"])
        page.fill("input[name='PatientPhone']", patient["phone"])

    except Exception as e:
        return status(
            "MISSING_PORTAL_FIELD",
            f"Patient field failure: {str(e)}",
            page="patient_information",
            step="field_mapping"
        )

    # Screenshot AFTER fill
    take_screenshot(page, "02_patient_information_filled")

    if not safe_click(page, "button:has-text('Next')"):
        return status(
            "CLICK_ACTION_FAILED",
            "Next button failed on Patient page",
            page="patient_information",
            step="next_click"
        )

    page.wait_for_load_state("networkidle")

    return None  # success → continue workflow
