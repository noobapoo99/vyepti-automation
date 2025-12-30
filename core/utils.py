import os

def status(code, message):
    print({"status_code": code, "message": message})

def take_screenshot(page, name):
    os.makedirs("screenshots", exist_ok=True)
    page.screenshot(path=f"screenshots/{name}.png")

def stop_before_submit(page):
    take_screenshot(page, "final_form_completed")
    print("⚠️ Stopping before submission — review the form.")
    input("Press Enter to close browser...")
