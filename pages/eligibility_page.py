from core.utils import take_screenshot


def select_yes_no_question(page, question_text, answer):
    option = "Yes" if str(answer).lower() == "yes" else "No"
    question = page.get_by_text(question_text, exact=False)
    question.locator(
        f".//label[normalize-space()='{option}']"
    ).click()


def select_dropdown(page, label_text, value):
    if value:
            page.get_by_label(label_text, exact=False).select_option(value)


def fill_text_field(page, label_text, value):
    if value:
        page.get_by_label(label_text, exact=False).fill(value)


def fill_eligibility(page, data):
    eligibility = data["eligibility"]
    patient = data.get("patient_information", {})
    facility = data.get("facility_information", {})
    address = patient.get("address", {})

    page.wait_for_selector("text=Patient Residence State")

    select_dropdown(
        page,
        "Patient Residence State",
        address.get("state")
    )

    select_dropdown(
        page,
        "Enrollment Site Type",
        "Physician Office"
    )

    fill_text_field(page, "Enrollment Site Name",
                    facility.get("name"))

    fill_text_field(page, "Enrollment Site Phone Number",
                    facility.get("phone"))

    fill_text_field(page, "Enrollment Site Fax Number",
                    facility.get("fax"))

    questions = [
        (
            "Is your patient 17 years of age or older?",
            eligibility["is_patient_17_or_older"]
        ),
        (
            "Has your patient been prescribed VYEPTI",
            eligibility["prescribed_for_fda_approved_indication"]
        ),
        (
            "Is your patient enrolled in a state or federally-funded",
            "No"
        ),
        (
            "Is your patient both Medicare-eligible and enrolled",
            "No"
        ),
        (
            "Is your patient self-pay or uninsured?",
            "No"
        ),
    ]

    for question_text, value in questions:
        select_yes_no_question(page, question_text, value)

    take_screenshot(page, "./../screenshots01_eligibility")

    page.click("text=NEXT")
    page.wait_for_load_state("networkidle")
