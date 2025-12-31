from core.utils import take_screenshot


def fill_patient_information(page, data):
    patient = data["patient_information"]
    address = patient.get("address", {})

    page.wait_for_selector("text=Patient Information")

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

    take_screenshot(page, "./../screenshots/02_patient_information")

    page.click("text=NEXT")
    page.wait_for_load_state("networkidle")
