import asyncio
import sys

if sys.platform.startswith("win"):
    # Use the older SelectorEventLoopPolicy on Windows instead of ProactorEventLoop
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
import pytest
from playwright.async_api import async_playwright

@pytest.mark.asyncio
async def test_login():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://the-internet.herokuapp.com/login")
        await page.fill("#username", "tomsmith")
        await page.fill("#password", "SuperSecretPassword!")
        await page.click("button.radius")
        content = await page.content()
        assert "Secure Area" in content
        await browser.close()
