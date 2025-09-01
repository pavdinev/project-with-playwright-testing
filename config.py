# config.py
# Minimal config template - adapt to your project

BASE_URL = "https://www.saucedemo.com/"
HEADLESS = False

# Users dictionary example - adapt to your real config
USERS = {
    "standard_user": {"username": "standard_user", "password": "secret_sauce"},
    "locked_out_user": {"username": "locked_out_user", "password": "secret_sauce"},
    "problem_user": {"username": "problem_user", "password": "secret_sauce"},
    "performance_glitch_user": {"username": "performance_glitch_user", "password": "secret_sauce"},
}
SCREENSHOT_DIR = "screenshots"