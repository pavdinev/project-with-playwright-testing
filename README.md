# SauceDemo Playwright (Python-only)

This project demonstrates UI automation using **Playwright for Python** with the **sync API** and **unittest**.

## Setup

```bash
python -m venv .venv
. .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python -m playwright install

## Run all tests
python run_tests.py

## Run single test
python -m unittest tests.test_login