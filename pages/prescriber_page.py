from core.utils import take_screenshot

def fill_prescriber_information(page, data):
    page.wait_for_selector("text=text=Referring Physician Information")
    page.fill("input[name='PhysicianFirstName']", data["first_name"])
    page.fill("input[name='PhysicianLastName']", data["last_name"])

    page.fill("input[name='PhysicianAddress1']", data["address"]["line1"])
    page.fill("input[name='PhysicianCity']", data["address"]["city"])
    # page.select_option("select[name='PhysicianState']", data["address"]["state"])
    page.locator("select[name='PhysicianState']").select_option(
        label=data["address"]["state"]
    )
    page.fill("input[name='PhysicianZIP']", data["address"]["zip"])

    page.fill("input[name='PhysicianOfficeNumber']", data["phone"])
    page.fill("input[name='PhysicianFaxNumber']", data["fax"])

    page.screenshot(path="./../screenshots/03_physician_information.png")
    page.click("text=NEXT")
    page.wait_for_load_state("networkidle")
