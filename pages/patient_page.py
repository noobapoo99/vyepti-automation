from core.utils import take_screenshot

def fill_patient_information(page, data):
    page.wait_for_selector("text=Patient Information")
    page.fill("input[name='PatientFirstName']", data["first_name"])
    page.fill("input[name='PatientLastName']", data["last_name"])

    page.fill("input[name='PatientAddress1']", data["address"]["line1"])
    page.fill("input[name='PatientCity']", data["address"]["city"]) 
    page.select_option("select[name='PatientState']", data["address"]["state"])
    page.fill("input[name='PatientZIP']", data["address"]["zip"])

    page.select_option("select[name='PatientGender']", data["gender"])
    page.fill("input[name='PatientDOB']", data["date_of_birth"])

    page.fill("input[name='PatientEmail']", data["email"])
    page.fill("input[name='PatientPhone']", data["phone"])
    take_screenshot(page, "./../screenshots/02_patient_information")
    page.click("text=NEXT")
    page.wait_for_load_state("networkidle")
