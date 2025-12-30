from core.utils import take_screenshot, stop_before_submit

def fill_primary_insurance(page, data):
    page.wait_for_selector("text=Insurance Information")
    page.select_option("select[name='InsuranceState']", "ILLINOIS")  # or from JSON
    page.fill("input[name='InsuranceCarrier']", data["insurance_name"])

    holder = data["policy_holder_name"].split(" ", 1)
    page.fill("input[name='PolicyHolderFirstName']", holder[0])
    page.fill("input[name='PolicyHolderLastName']", holder[1])

    page.fill("input[name='PolicyNumber']", data["member_id"])
    page.fill("input[name='GroupNumber']", data["group_id"])

    take_screenshot(page, "04_insurance_filled")
    stop_before_submit(page)
