# QA Automation Portfolio Project

## Overview

This project demonstrates a complete **end-to-end QA automation framework** built using **Python, Playwright, and pytest**. It covers UI, API, and database testing, including:

- Functional UI automation using Playwright
- API testing with Playwright's APIRequestContext
- SQLite database validation to verify backend data integrity
- Data-driven tests with JSON/CSV inputs
- Cross-browser testing (Chromium, Firefox, WebKit)
- HTML test reports with screenshots
- CI/CD integration with GitHub Actions

---

## Tech Stack

- Python 3.9+  
- Playwright for UI & API automation  
- Pytest test runner and pytest-html for reporting  
- SQLite database for lightweight DB testing  
- GitHub Actions for CI/CD  

---

## Project Structure

```
qa-portfolio-project/
├── tests/                  # UI, API, and DB test scripts  
├── data/                   # Test data files (JSON, CSV)  
├── utils/                  # Helper modules (API, UI, DB)  
├── db/                     # SQLite DB file  
├── reports/                # Test reports and screenshots  
├── .github/workflows/      # CI pipeline config  
├── requirements.txt        # Python dependencies  
├── playwright.config.py    # Playwright config  
└── README.md               # This file  
```

---

## Setup Instructions

1. Clone the repo:  
   ```bash
   git clone https://github.com/yourusername/qa-portfolio-project.git
   cd qa-portfolio-project
   ```

2. Create & activate a virtual environment:  
   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/macOS  
   venv\Scripts\activate       # Windows
   ```

3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

4. Run tests:  
   ```bash
   pytest
   ```

---

## CI/CD

GitHub Actions pipeline is configured to run tests on each push and pull request. Test reports are saved as workflow artifacts.

---

## Extending the Project

- Add more comprehensive UI workflows  
- Integrate visual regression and accessibility tests  
- Expand database validation to cover complex scenarios  
- Include performance testing with locust or pytest-benchmark  

---

## Contact

Pavel Dinev  
Email: pavel.r.dinev@gmail.com  
LinkedIn: [linkedin.com/in/pavel-dinev-ba4434290](https://linkedin.com/in/pavel-dinev-ba4434290)  
GitHub: [github.com/pavdinev](https://github.com/pavdinev)
