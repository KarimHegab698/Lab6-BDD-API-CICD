import os
import allure
import requests
from allure_commons.types import AttachmentType

# 1x1 placeholder PNG (API tests have no browser to screenshot)
PLACEHOLDER_PNG = bytes.fromhex(
    "89504e470d0a1a0a0000000d4948445200000001000000010802000000907753de"
    "0000000c49444154789c63f8cfc0000003010100c9fe92ef"
    "0000000049454e44ae426082"
)


def after_scenario(context, scenario):
    # Check if the scenario failed
    if scenario.status == "failed":
        try:
            # Capture screenshot (placeholder instead of context.page.screenshot)
            os.makedirs("screenshots", exist_ok=True)
            screenshot_path = f"screenshots/{scenario.name.replace(' ', '_')}.png"
            with open(screenshot_path, "wb") as f:
                f.write(PLACEHOLDER_PNG)

            # Attach screenshot to Allure report
            with open(screenshot_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name=scenario.name,
                    attachment_type=AttachmentType.PNG
                )
        except Exception as e:
            print(f"Failed to take screenshot: {e}")

    # Clean up any bin left behind on JSONBin
    bin_id = getattr(context, "bin_id", None)
    if bin_id and not getattr(context, "bin_deleted", False):
        try:
            requests.delete(
                f"https://api.jsonbin.io/v3/b/{bin_id}",
                headers={"X-Master-Key": os.getenv("JSONBIN_MASTER_KEY", "")},
                timeout=30
            )
        except requests.RequestException:
            pass

    # Don't forget to close your browser page/context if you are using Playwright/Selenium
    if hasattr(context, 'page'):
        context.page.close()