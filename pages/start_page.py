from core.utils import safe_click, status

def enter_hcp_portal(page):

    try:
        page.wait_for_selector("text=HEALTHCARE PROFESSIONAL", timeout=12000)
    except:
        return status(
            "PAGE_LOAD_TIMEOUT",
            "Landing page did not load",
            page="landing_page",
            step="wait_for_page"
        )

    try:
        safe_click(page, "text=HEALTHCARE PROFESSIONAL")
        page.wait_for_load_state("networkidle")
    except:
        return status(
            "CLICK_ACTION_FAILED",
            "Failed to click Healthcare Professional",
            page="landing_page",
            step="entry_click"
        )

    return None   # success
