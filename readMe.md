# Vyepti Copay Portal Automation — Playwright (Python)

This project automates the **Vyepti Connect Copay Assistance Portal** workflow using Playwright — filling the form step‑by‑step and **stopping safely before final submission**.

The automation is designed to:

- mimic human interaction behavior
- surface failures using structured `status_code` responses
- capture screenshots for each page
- stop before submission to avoid creating real program enrollments

---

## 🖥️ Tech Stack

- Python 3.10+
- Playwright (sync API)
- Chromium browser
- Modular page‑object structure
- JSON‑driven field mapping

---

## 📂 Project Structure

```
vyepti-automation/
│
├── automation.py                # main entry workflow
├── core/
│   ├── browser.py               # browser launcher
│   ├── utils.py                 # helpers + status logger
│
├── pages/
│   ├── start_page.py            # landing page → HCP entry
│   ├── eligibility_page.py      # eligibility form
│   ├── patient_page.py          # patient details
│   ├── prescriber_page.py       # prescriber information
│   ├── insurance_page.py        # insurance + STOP before submit
│
├── data/
│   └── input_data.json          # form input source
│
└── screenshots/                 # saved screenshots
```

---

## ⚙️ Installation & Local Setup

### 1️⃣ Create & activate virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux

# or Windows
venv\Scripts\activate
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Install Playwright browsers

```bash
playwright install chromium
```

> Chromium is used in headed mode for review visibility.

---

## 🧾 Configure Input Data

Edit:

```
data/input_data.json
```

Example fields

```json
{
  "patient_information": {
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1964-08-17",
    "gender": "Male"
  },
  "eligibility": {
    "is_patient_17_or_older": "Yes",
    "prescribed_for_fda_approved_indication": "Yes"
  }
}
```

State & dropdown selections must match available portal options.

---

## ▶️ Run Automation

Run in **headed mode** (recommended while testing):

```bash
python automation.py
```

The script will:

1. open the Vyepti portal
2. enter **Healthcare Professional** workflow
3. complete each page
4. capture screenshots
5. **stop safely before submission**

A final prompt will appear:

```
⚠️ Stopping before submission — review the form.
Press Enter to close browser...
```

Press Enter when finished reviewing.

---

## 🧩 Status Code Outputs

The script prints structured status logs such as:

```
{
  "status_code": "SUCCESS_FORM_COMPLETED",
  "page": "insurance_information",
  "step": "stop_before_submit"
}
```

Other classifications include:

| Code                   | Meaning                                      |
| ---------------------- | -------------------------------------------- |
| `PAGE_LOAD_TIMEOUT`    | portal page did not load                     |
| `MISSING_PORTAL_FIELD` | expected field was not found                 |
| `CLICK_ACTION_FAILED`  | radio / checkbox / button interaction failed |
| `INVALID_FIELD_VALUE`  | dropdown value not present                   |
| `UNKNOWN_ERROR`        | uncaught runtime exception                   |

These help reviewers understand **where & why** failure occurred.

---

## 🖼️ Screenshots

Stored automatically in:

```
/screenshots
```

Screenshots are captured:

- after each page completes
- before STOP‑before‑submit

---

## 🔒 Safety Controls

The automation includes:

✔ NO submission is performed  
✔ Execution halts on final page  
✔ Form is left populated for review  
✔ User must manually exit

This is intentional to prevent real case creation.

---

## 🧪 Debug Mode (Optional)

Enable inspector:

```bash
PWDEBUG=1 python automation.py
```

This allows:

- DOM inspection
- locator validation
- replaying interactions

---

## 🙋 Support Notes

If a field fails due to portal layout differences:

- review screenshot
- inspect field DOM
- update selector in `/pages/*` file

Selectors intentionally prioritize:

- human‑like interaction
- semantic roles
- explicit page intent

---

## ✅ Expected Reviewer Experience

When executed successfully, reviewers will see:

- browser running in headed mode
- fields populate step‑by‑step
- screenshots saved
- safety stop at final page
- structured status log output

---

## 📄 Author Notes

Built as part of the **AI Automation Intern Assignment**.

Emphasis placed on:

- UX‑aware automation practices
- resilient selector design
- safety & validation logic
- meaningful failure reporting

---
